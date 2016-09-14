__author__ = 'Kienka Cromwell KIO'
import bottle
from pymongo import MongoClient

import json
import re
from random import randint
@bottle.route('/map')
def tweet_map():
    #make a connection to pymongo to obtain all coordinate points
    connection = MongoClient('localhost',27017)
    db = connection.testerDB
    tweets = db.tweets
    cursor = db.tweets.find({"tweet.place.coordinates":{"$exists":True}},{"tweet.place.coordinates":1,"tweet.text":1,"_id":0})
    points = []
    for doc in cursor:
        #txt =[doc['tweet']['text']]
        point=doc['tweet']['place']['coordinates']
        #point_tweet= point+txt
        points.append(point)
    #points =points[-10000:]
    return bottle.template('tweet_mapping.tpl',points=points)

@bottle.route('/wordcloud')
def cloud():
    #make a connection to pymongo to obtain all coordinate points
    '''
    connection = MongoClient('localhost',27017)
    db = connection.testerDB
    tweets = db.tweets
    cursor = db.tweets.find({"tweet.text":{"$exists":True}},{"tweet.text":1,"_id":0})
    points = []
    phrases=""
    for doc in cursor:
        txt =doc['tweet']['text']
        points.append(txt)
    #Take only the last 500 tweets
    points= str(json.dumps(points[-500:]))
    phrases= re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','',str(points).rstrip(']').lstrip('['),flags=re.MULTILINE)
    #phrases = re.sub(r'[^\x00-\x7F]+|\\ud...','',phrases,flags=re.MULTILINE)
    phrases=phrases.decode('unicode_escape').encode('ascii','ignore')
    '''

    return bottle.template("Wcloud.tpl", name="Mappy")


bottle.debug(True)
bottle.run(host='localhost', port=8080)