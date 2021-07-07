import json

data = json.load(open('./main/src/reddit_jokes.json'))
my_jokes = []
count = 0
for d in data:
    if d['score'] >10:
        my_jokes.append(d)
        count = count +1


json.dump(my_jokes,open('my_jokes.json','w+'))

