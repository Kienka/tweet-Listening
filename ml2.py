__author__ = 'Kienka Cromwell KIO'
__author__ = 'Kienka Cromwell KIO'
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from pymongo import MongoClient
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re
from nltk.classify import ClassifierI
from statistics import mode
from nltk.corpus import wordnet
import random

from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = float(choice_votes) / float(len(votes))
        return conf

stop_words = stopwords.words('english')
connection = MongoClient('localhost', 27017)
db = connection.testerDB
tweets = db.tweets

cursor = db.tweets.find({"$text":{"$search":"data network mtn etisalat airtel globacom glo internet wifi"}
                            ,"tweet.tag" :{"$exists":True}})
'''
#for network standards
cursor = db.tweets.find({"$text":{"$search":"data network internet wifi"}
                            ,"tweet.network_standard" :{"$exists":True}})
'''

tweet_documents=[]
for doc in  cursor:
    tweet_words= doc['tweet']['text']
    #removing all links
    tweet_words= re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','',tweet_words,flags=re.MULTILINE)
    #removing punctuations
    tweet_words = re.sub(r'\p{P}(?<![\-@#])','',tweet_words,flags=re.MULTILINE)
    tweet_words= tweet_words.lower()



    tokenizer = TweetTokenizer(preserve_case=False)
    tweet_words = tokenizer.tokenize(tweet_words)
    #remove words with lenght of one character
    #tweet_words = [word for word in tweet_words if len(word) > 1]
    #remove stop words
    #tweet_words = [w for w in tweet_words if w not in stop_words]
    tweet_tag=doc['tweet']['tag']
    tweet_documents.append((tweet_words,tweet_tag))

random.shuffle(tweet_documents)
#print tweet_documents[0]

#Obtaining all words

all_words =[]
for l in tweet_documents:
    all_words=all_words + l[0]

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:700]

#print word_features
def find_features(document):
    words = set(document)
    features = {}
    #Prune stop words and single character
    #words = [w for w in words if w not in stop_words]
    #words = [word for word in words if len(word) > 1]
    for w in word_features:
        features[w]=(w in words)
        #print features[w]
    return features
def find_features2(documents):
    words = set(documents)
    words = list(words)
    features = {}
    s=[] #synonyms
    #remove stop words
    words = [w for w in words if w not in stop_words]
    words = [word for word in words if len(word) > 1]
    for w in words:
        for syn in wordnet.synsets(w):
            for l in syn.lemmas():
                s.append(l.name())
    words=list(set(words + s))
    for w in word_features:
        features[w]=(w in words)
        #print features[w]
    return features


#Clean the tweets

#print find_features(movie_reviews.words('neg/cv000_29416.txt'))
#featuresets = [(find_features(rev),tag) for (rev,tag) in tweet_documents]
featuresets= [(find_features(rev),tag) for (rev,tag) in tweet_documents]
#print featuresets
print featuresets[1][0]

#training
training_set = featuresets[:500]
testing_set = featuresets[100:]

from sklearn.feature_extraction.text import CountVectorizer
clf = MultinomialNB().fit(training_set)