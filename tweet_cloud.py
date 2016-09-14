__author__ = 'Kienka Cromwell KIO'

from pymongo import MongoClient
import bottle


@bottle.route('/wordcloud')
def cloud():
    #make a connection to pymongo to obtain all coordinate points
    connection = MongoClient('localhost',27017)
    db = connection.testerDB
    tweets = db.tweets
    cursor = db.tweets.find({"tweet.text":{"$exists":True}},{"tweet.text":1,"_id":0})
    #points = []
    #phrases=""
    #for doc in cursor:
     #   txt =doc['tweet']['text']

        #points.append(txt)
    #Take only the last 500 tweets
    #points= json.dumps(points[-500:])
    #phrases= re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','',str(points).rstrip(']').lstrip('['),flags=re.MULTILINE)
    #phrases = re.sub(r'[^\x00-\x7F]+|\\ud...','',phrases,flags=re.MULTILINE)
    #phrases=phrases.decode('unicode_escape').encode('ascii','ignore')

    return bottle.template("tweet_cloud", words=phrases)
bottle.debug(True)
bottle.run(host='localhost', port=8080)