from __future__ import division
_author__ = 'Kienka Cromwell KIO'

from itertools import *
from pylab import *
from nltk.corpus import brown
from string import lower
from collections import Counter
from pymongo import MongoClient
from nltk.tokenize import TweetTokenizer
import re

connection = MongoClient('localhost', 27017)
db = connection.testerDB
tweets = db.tweets

cursor = db.tweets.find({}).limit(50000)
tweet_documents=[]
for doc in  cursor:
    tweet_words= doc['tweet']['text']
    #tweet_words= tweet_words.lower()
    tokenizer = TweetTokenizer()
    #tweet_words= re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','',tweet_words,flags=re.MULTILINE)
    #tweet_words = re.sub(r'\p{P}(?<![\-@#])','',tweet_words,flags=re.MULTILINE)
    #tweet_words= tweet_words.lower()
    tweet_words = tokenizer.tokenize(tweet_words)
    #removing punctuations

    tweet_documents=tweet_documents+tweet_words
# The data: token counts from the Brown corpus
print len(brown.words())
print len(tweet_documents)
tokens_with_count = Counter(imap(lower,tweet_documents))
counts = array(tokens_with_count.values())
tokens = tokens_with_count.keys()

# A Zipf plot
ranks = arange(1, len(counts)+1)
indices = argsort(-counts)
frequencies = counts[indices]
loglog(ranks, frequencies)

title("Zipf plot for Brown corpus tokens")
xlabel("Frequency rank of token")
ylabel("Absolute frequency of token")
grid(True)
for n in list(logspace(-0.5, log10(len(counts)), 20).astype(int)):
    dummy = text(ranks[n], frequencies[n], " " + tokens[indices[n]],
                 verticalalignment="bottom",
                 horizontalalignment="left")

show()
