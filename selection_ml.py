__author__ = 'Kienka Cromwell KIO'

from pymongo import MongoClient
import sys
import codecs

connection = MongoClient('localhost',27017)
db = connection.testerDB
tweets = db.tweets
#FOR General tweet tag

cursor = db.tweets.find({"$text":{"$search":"President Buhari"}
                            ,"tweet.pres_tag" :{"$exists":False},"tweet.entities.urls":[]})
'''
#for network standards
cursor = db.tweets.find({"$text":{"$search":"data network internet wifi"}
                            ,"tweet.tag" :{"$exists":False},"tweet.entities.urls":[]})
                            '''
for doc in cursor:
    try:
        tweet= doc['tweet']['text'].decode('utf-8')
        print tweet
        id = doc['_id']
        tag = input("Enter a tag for this tweet [0 or 1 or 2]: ")
        while not (tag==1 or tag==0 or tag==2):
            tag=input("Please you must Enter 0 or 1 as response : ")
        db.tweets.update_one({"_id":id},{"$set":{"tweet.pres_tag":tag}})

    except UnicodeEncodeError :
        continue
    #break
    #db.tweets.find_
    #Take an input the data the tag

