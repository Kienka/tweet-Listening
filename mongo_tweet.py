__author__ = 'Kienka Cromwell KIO'

import pymongo
from pymongo import MongoClient
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import collections
from random import randint


access_token = "XXXXX"
access_token_secret = "XXXXX"
consumer_key = "XXXXXX"
consumer_secret = "XXXXXXXX"

class StdOutListener(StreamListener):

    def on_data(self, data):
        mdata=json.loads(data)

        #print mdata['entities'].keys()
        location= 'null' if mdata['user']['location'] is None else mdata['user']['location']
        cords='null' if mdata['coordinates'] is None else mdata['coordinates']['coordinates']
        place='null' if mdata['place'] is None else mdata['place']
        usr_lang='null' if mdata['user']['lang'] is None else mdata['user']['lang']

        tweet_data = {"user":
                          {"name":mdata['user']['name'],
                           "location":location,
                           "user_id":mdata['user']['id_str'],
                            "screen_name":mdata['user']['screen_name'],
                            "user_created_at":mdata['user']['created_at'],
                            "language":usr_lang
                            },
                      "tweet":
                          {
                              "text":mdata['text'],
                              "created_at":mdata['created_at'],
                              "place": {
                                  "country_code":place['country_code'],
                                  "country":place['country'],
                                  "coordinates":place['bounding_box']['coordinates'][0][randint(0,2)]

                              },
                              "coordinates":cords,
                              "entities":{
                                  "user_mentions":mdata['entities']['user_mentions'],
                                  "hashtags":mdata['entities']['hashtags'],
                                  "urls":mdata['entities']['urls']
                              },
                              "tweet_id":mdata['id_str'],
                              "language":mdata['lang'],
                              "timestamp":mdata['timestamp_ms']

                          }
                      }
        #print tweet_data

        #Inserting data to MongoDB
        connection = MongoClient("mongodb://localhost")
        db = connection.testerDB
        tweets = db.tweets

        try:
            tweets.insert_one(tweet_data)
            print "A new row inserted #tweet!"
        except Exception as e:
            print "Unexpected error:", type(e), e
        #f1=open('./tweet_data8.txt', 'a')
        #json.dump(data,f1)
        #print>>f1.write(data)
        return True

    def on_error(self, status):
        print status
        return True
#Stream Tweets and Load to MongoDB
if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    places = api.geo_search(query="Nigeria", granularity="country")
    stream = Stream(auth, l)

    #This line filter Twitter Streams by long and Lat to capture tweets in Nigeria
    coords=[places[0].bounding_box.coordinates[0][0][0],places[0].bounding_box.coordinates[0][0][1]
        ,places[0].bounding_box.coordinates[0][1][0],places[0].bounding_box.coordinates[0][1][1]\
        ,places[0].bounding_box.coordinates[0][2][0],places[0].bounding_box.coordinates[0][2][1]\
        ,places[0].bounding_box.coordinates[0][3][0],places[0].bounding_box.coordinates[0][3][1]\
        ,places[0].bounding_box.coordinates[0][0][0],places[0].bounding_box.coordinates[0][3][1]\
        ,places[0].bounding_box.coordinates[0][4][0],places[0].bounding_box.coordinates[0][4][1]]
    print coords
    coords = [ round(elem,2)for elem in coords ]
    print coords
    #coords2=[2.0,4.0,14.0,15.0]
    coords3=[2.67, 4.2, 13.89, 14.68]
    stream.filter(locations=coords3)
