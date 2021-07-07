import json
import string
import random 
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer 
import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import Dense, Dropout
import requests



nltk.download("punkt")
nltk.download("wordnet")

from src.intent_handlers import handle_research, handle_jokes, handle_music, rm_stop_words



words = []
classes = []
y = []
x = []
data = []
questions = []
context = {}

def read_json():
    data = []
    data = json.load(open('./main/src/intent.json'))
    return data

lemmer = WordNetLemmatizer()

def cleaner():
    data = read_json()
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            x.append(pattern)
            y.append(intent["tag"])
        
    # add the tag to the classes if it's not there already 
        if intent["tag"] not in classes:
            classes.append(intent["tag"])
    pass


def trainer():
    training = []
    out_empty = [0] * len(classes)# creating the bag of words model
    for idx, doc in enumerate(x):
        bow = []
        text = lemmer.lemmatize(doc.lower())
        for word in words:
            bow.append(1) if word in text else bow.append(0)    # mark the index of class that the current pattern is associated
        # to
        output_row = list(out_empty)
        output_row[classes.index(y[idx])] = 1    # add the one hot encoded BoW and associated classes to training 
        training.append([bow, output_row])# shuffle the data and convert it to an array
    random.shuffle(training)
    training = np.array(training, dtype=object)# split the features and target labels
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

        # defining some parameters
    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    epoch = 15400# the deep learning model 2400 works
    l_rate = 0.0001 #0.001 works
    model = Sequential()
    model.add(Dense(1500, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(output_shape, activation = "softmax"))
    adam = tf.keras.optimizers.Adam(learning_rate=0.001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',
                optimizer=adam,
                metrics=["accuracy"])
    print(model.summary())
    model.fit(x=train_X, y=train_y, epochs=epoch, verbose=1)
    model.save('./intent.mdl')
    pass

def clean_text(text): 
  tokens = nltk.word_tokenize(text)
  tokens = [lemmer.lemmatize(word) for word in tokens]
  return tokens

def bag_of_words(text, vocab): 
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens: 
        for idx, word in enumerate(vocab):
            if word == w: 
                bow[idx] = 1
    return np.array(bow)

def pred_class(text, vocab, labels): 
    model = []
    try:
        model = tf.keras.models.load_model('intent.mdl')
        pass
    except:
        trainer()
        model = tf.keras.models.load_model('intent.mdl')
        pass
    model = tf.keras.models.load_model('intent.mdl')
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.6
    # for i, r in enumerate(result):
        # print(r,classes[i])
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list

def get_response(intents_list, intents_json,context):
    result = ""
    tag = intents_list[0]
    list_of_intents = intents_json["intents"]
    dt = {}
    for i in list_of_intents:
        dt = i
        if i["tag"] == tag:
            if not i['context_filter'][0] and not context:
                result = random.choice(i["responses"])
                break
            elif context and i['context_filter'][0]:
                if context['context'] == i['context_filter'][0]:
                    result = random.choice(i['responses'])
                    break
            elif i['context_filter'][0] and not context:
                tag = i['context_filter'][0]
                continue
            elif context and not i['context_filter'][0]:
                result = random.choice(i['responses'])
                break
    if dt['context'][0]:
        context['context'] = dt['context'][0]
    
    print(context)
    return (result,dt['tag'])

def q_bot(message):
    offline = True
    try:
        requests.get("http://google.com")
        offline = False
    except requests.exceptions.ConnectionError as e:
        offline = True
        pass
    l_data = read_json()
    temp_message = message
    # message = rm_stop_words(message)
    questions.append(message)
    if len(questions) <= 1:
        cleaner()
    elif len(questions) > 2:
        questions.pop()
    intents = pred_class(message, words, classes)
    resp, intent = get_response(intents, l_data,context)
    if 'research' in intent:
        result = handle_research(temp_message)
    elif 'jokes' in intent:
        result = handle_jokes()
    elif 'music' == intent:
        # context['context'] = 'music'
        result = handle_music(temp_message,offline)
        
    else:
        result = {"type":"text","data":resp,"action":[intent],'extra_info':""}
    
    return result


if __name__ == "__main__":
    print(q_bot("Hi"))
    pass