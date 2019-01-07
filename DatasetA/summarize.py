import pandas as pd
import re
from nltk.stem import PorterStemmer
import math

from DatasetA.index import summarization
from DatasetA.topics import implementLDA


def tweets_to_clusters():

    x = pd.read_csv("mytweet2",)
    print(x['text'])

    y = pd.read_csv("t1_0.5t2_0.32.csv",)
    print(y["tweetd"])

    tweets = {}
    merged = pd.merge(y, x,left_on='tweetd', right_on='id')

    col = ['tweets','clusterID']
    df = pd.DataFrame(columns=col)
    df['tweets']=merged['text']
    df['clusterID']=merged['clusterno']
    df.to_csv('out.csv')
def intregation():
     tweets_to_clusters()
     implementLDA()
     summarization()