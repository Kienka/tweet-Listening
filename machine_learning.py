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
'''
cursor = db.tweets.find({"$text":{"$search":"data network mtn etisalat airtel globacom glo internet wifi"}
                            ,"tweet.tag" :{"$exists":True}})
'''
#for network standards
cursor = db.tweets.find({"$or":[{"tweet.pres_tag":0},
                                 {"tweet.pres_tag":1}]})
#db.tweets.find({$or:[{"tweet.pres_tag":0},{"tweet.pres_tag":1}]})


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
    tweet_tag=doc['tweet']['pres_tag']
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
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

Randf_classifier = SklearnClassifier(RandomForestClassifier())
Randf_classifier.train(training_set)
print 'RandomForest Classifier Accuracy percent: ',(nltk.classify.accuracy(Randf_classifier,testing_set))*100
#print 'RandomForest Classifier Precision percent: ',(nltk.precision(set(Randf_classifier),set(testing_set)))*100
'''
Bagging_classifier = SklearnClassifier(BaggingClassifier(MultinomialNB()))
Bagging_classifier.train(training_set)
print 'Bagging Classifier Accuracy percent: ',(nltk.classify.accuracy(Bagging_classifier,testing_set))*100

knn_classifier = SklearnClassifier(KNeighborsClassifier())
knn_classifier.train(training_set)
print 'KNN Classifier Accuracy percent: ',(nltk.classify.accuracy(knn_classifier,testing_set))*100
'''
voted_classifier = VoteClassifier(classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier
                                  )
print "voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100
'''
print "Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100
print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)
'''
#checking indvidual tweets
#i am disgusted with this airtel data shit network
test_tweet=["i","love","my","President"]
test_tweet2=["President","buhari","should","quit","and","stop","blabbing","rubbish"]
test_tweet3=["Welcome","back","mr","President"]
test_tweet4=['Buhari','is', 'incompetent', 'and','I','am','sad']
test_tweet5 =["no","love","for","APC","President","lied"]
print voted_classifier.classify(find_features(test_tweet)), "Confidence",voted_classifier.confidence(find_features(test_tweet))*100
print voted_classifier.classify(find_features(test_tweet2)), "Confidence",voted_classifier.confidence(find_features(test_tweet2))*100
print voted_classifier.classify(find_features(test_tweet3)), "Confidence",voted_classifier.confidence(find_features(test_tweet3))*100
print voted_classifier.classify(find_features(test_tweet4)), "Confidence",voted_classifier.confidence(find_features(test_tweet4))*100
print voted_classifier.classify(find_features(test_tweet5)), "Confidence",voted_classifier.confidence(find_features(test_tweet5))*100
print "Random Forest"
print Randf_classifier.classify(find_features(test_tweet))
print Randf_classifier.classify(find_features(test_tweet2))
print Randf_classifier.classify(find_features(test_tweet3))
print Randf_classifier.classify(find_features(test_tweet4))
print Randf_classifier.classify(find_features(test_tweet5))

print "Naive Bayes"
print classifier.classify(find_features(test_tweet))
print classifier.classify(find_features(test_tweet2))
print classifier.classify(find_features(test_tweet3))
print classifier.classify(find_features(test_tweet4))
print Randf_classifier.classify(find_features(test_tweet5))

voted_classifier2 = VoteClassifier(MNB_classifier,
                                   SGDClassifier_classifier,
                                   NuSVC_classifier,
                                   Randf_classifier,
                                   LinearSVC_classifier)

#print voted_classifier2

print "voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier2, testing_set))*100
print voted_classifier2.classify(find_features(test_tweet)), "Confidence",voted_classifier2.confidence(find_features(test_tweet))*100
print voted_classifier2.classify(find_features(test_tweet2)), "Confidence",voted_classifier2.confidence(find_features(test_tweet2))*100
print voted_classifier2.classify(find_features(test_tweet3)), "Confidence",voted_classifier2.confidence(find_features(test_tweet3))*100
print voted_classifier2.classify(find_features(test_tweet4)), "Confidence",voted_classifier2.confidence(find_features(test_tweet4))*100
print voted_classifier2.classify(find_features(test_tweet5)), "Confidence",voted_classifier2.confidence(find_features(test_tweet5))*100
#print voted_classifier.confidence(test_tweet3)*100