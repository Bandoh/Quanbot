import nltk
import wikipedia
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from youtube import Search
from os import listdir
from pytube import YouTube
import bs4
from youtubesearchpython import VideosSearch
from difflib import SequenceMatcher
nltk.download("stopwords")
nltk.download("punkt")

stop_words = set(stopwords.words('english'))

def youtuber_searcher(q):
    q.replace(" ","+")
    url = 'https://www.youtube.com/results?search_query={}'.format(q)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text,features="html.parser")
    ln = soup.find_all('div')
    # print(ln)
    # print(resp.text)
    pass


def rm_punct(message):
    words = nltk.word_tokenize(message)
    new_words= [word for word in words if word.isalnum()]
    return " ".join(new_words)

def rm_stop_words(message):
    result = []
    word_tokens = word_tokenize(message)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    return " ".join(filtered_sentence)

def handle_research(message):

    try:
        result = wikipedia.summary(rm_stop_words(message),sentences=1)
    except wikipedia.exceptions.DisambiguationError as e :
        result = "Please be specific {}".format(e)
    except requests.exceptions.ConnectionError as n :
        result = "I am not connected to the internet currently so i cannot help you..."
    return {"type":"text","data":result}


def handle_jokes():
    url = "https://official-joke-api.appspot.com/jokes/random"
    r = requests.get(url).json()
    result = r['setup']+" "+ r['punchline']
    return {"type":"text","data":result}


def handle_weather():
    url='https://fcc-weather-api.glitch.me/api/current?lat=5.6064892&lon=-0.080084'


def handle_music(message,offline):
    if not offline:
        yt_url = 'https://www.youtube.com/watch?v='
        
        r = VideosSearch(message)
        result = r.result()['result']
        print(result[0]['thumbnails'])
        file_name = rm_punct((result[0]['title'])).lower().replace(" ","_")
        link = yt_url+result[0]['id']
        all_files = listdir('../bot_ui/public/media/music')
        found = False
        for f in all_files:
            if "{}.mp4".format(file_name) in f:
                found = True
        if not found:
            YouTube(link).streams.filter(only_audio=True).first().download('../bot_ui/public/media/music',file_name)
            pass
    else:
        m_words = word_tokenize(message)
        all_files = listdir('../bot_ui/public/media/music')
        current_ratio = 0
        for f in all_files:
            rat = SequenceMatcher(None,message,f).ratio() 
            if rat >= current_ratio:
                current_ratio = rat
                file_name = f.replace(".mp4","")
                
        pass
    return {"type":"mp3","data":"/media/music/{}.mp4".format(file_name),"extra_info":[file_name.replace("_"," ").capitalize()],'action':['music']}


