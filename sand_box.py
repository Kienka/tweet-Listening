__author__ = 'Kienka Cromwell KIO'
from pymongo import MongoClient
import re
import json
import nltk
from nltk import TweetTokenizer,FreqDist,bigrams
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

#make a connection to pymongo to obtain all coordinate points
connection = MongoClient('localhost',27017)
db = connection.testerDB
tweets = db.tweets
cursor = db.tweets.find({"tweet.place.coordinates":{"$exists":True}},{"tweet.place.coordinates":1,"tweet.text":1,"_id":0})
points = []
phrases=""
for doc in cursor:
    txt =doc['tweet']['text']
    points.append(txt)

#cleaning the tes
points= str(json.dumps(points[-500:]))
#print points
#print points
#removing links
phrases= re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','',str(points).rstrip(']').lstrip('['),flags=re.MULTILINE)
#removing punctuations
phrases = re.sub(r'\p{P}(?<![\-@#])','',phrases,flags=re.MULTILINE)
#removing ascii cods
phrases=phrases.decode('unicode_escape').encode('ascii','ignore')
#print phrases

#removing all punctuations
#exclude = set(string.punctuation)
#phrases = ''.join(ch for ch in phrases if ch not in exclude)
#Getting all stopwords in English
nigerian_stopwords=['...','..','na','dey','lol','de','ur','let',"don't",'->',"i'm",
                    'go','one','know','say','ok','okay','really','like','maybe',
                    '#np','np','see','make',"he's",'dont','lmao','oh','ya',"it's",'en','lot','rt',
                    'yeah','always',"didn't","can't",'np_',"that's",'get','ft',
                    'keep','said','cc','give','help','pls','please','tell',
                    'many','ye','going','got','come','start','every','even','still',
                    'us','want','back','take','need','last','good','much','made','never',
                    'love','thank','god']
stop_words = stopwords.words('english')+nigerian_stopwords+stopwords.words('french')
#TweetTokenizer
tokenizer = TweetTokenizer(preserve_case=False)
phrases = tokenizer.tokenize(phrases)
#remove words with lenght of one character
phrases = [word for word in phrases if len(word) > 1]
#print phrases
words = [w for w in phrases if w not in stop_words]
term_bigram = bigrams(phrases)
print term_bigram
words=json.dumps(words)
words_text = "".join(words)
print words_text
#filtered_words = [word for word in phrases if word not in stopwords.words('english')]

#WORD CLOUD
wordcloud = WordCloud(background_color="white", max_words=2000).generate(str(words_text))
plt.figure(figsize=(30,30))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

phrases_dist= FreqDist(w.lower() for w in phrases if w not in stop_words)
hashtags=[h for h in phrases_dist.most_common(1000) if h[0].startswith('#')]
mentions=[m for m in phrases_dist.most_common(1000) if m[0].startswith('@')]
#terms=[w for w in phrases_dist.most_common(100)  if not w[0].startswith('#') or not w[0].startswith('@') ]
print hashtags
print mentions
print phrases_dist.most_common(100)

hashtags_df = pd.DataFrame(hashtags,columns=['Hashtags','Count'])
mentions_df = pd.DataFrame(mentions,columns=['Mentions','Count'])
terms_df = pd.DataFrame(phrases_dist.most_common(20),columns=['Terms','Count'])

hashtags_df.set_index(['Hashtags'],inplace=True)
mentions_df.set_index(['Mentions'],inplace=True)
terms_df.set_index(['Terms'],inplace=True)

hashtags_df.head(10).plot.bar()
plt.legend
plt.show()

mentions_df.head(10).plot.bar()
plt.legend
plt.show()

terms_df.plot.bar()
plt.show()



