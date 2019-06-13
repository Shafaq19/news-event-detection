import csv
import re
import pandas as pd
from collections import defaultdict
import time
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer
from py4j.java_gateway import JavaGateway

import numpy
from collections import Counter as mset

from MainFolder.EventDetection.index import summarization
from MainFolder.EventDetection.tagging import TopicCategorization

"""""""""""""""""""""
similarity score parameters a,b,c,d
"""""""""""""""""""""
a =  float(1/11)  # commen Noun
b = float(5/11)  # properNoun
c =  float(1/11) # verb
d = float(4/11) # hashtag threshold
threshold = 0.16
threshold2 = 0.3


threshold3=.4
"""""""""""""""
Initializing NER model and files input
"""""
gateway = JavaGateway()  # connect to the JVM
inputFile="../Data/mytweet02.csv"
Alltweets = pd.read_csv(inputFile, ",")
# print(len(Alltweets))
Outfilename = "../MyOutputs/clustersIds.csv"
output = open(Outfilename, mode='wt', encoding='utf-8')
fieldnames = ['clusterno', 'tweetd']
writer = csv.DictWriter(output, fieldnames=fieldnames,quoting=csv.QUOTE_MINIMAL)
writer.writeheader()
# File path which consists of Abbreviations.
fileName = "../utils/slang.txt"#
#  File Access mode [Read Mode]
accessMode = "r"
abbrRemov={}
with open(fileName, accessMode) as m:
    dataFromFile = csv.reader(m, delimiter="=")
    #print(dataFromFile)
    for row in dataFromFile:
        abbrRemov[row[0]]=row[1]
""""""""""""""""
preproceessing variable and functions
"""""
lmtz=WordNetLemmatizer()
stem=PorterStemmer()

def translator(user_string):
    # Check if selected word matches short forms[LHS] in text file.
    if user_string.upper() in abbrRemov.keys():
        # If match found replace it with its appropriate phrase in text file.
        user_string = abbrRemov[user_string.upper()];
    return user_string
def tweetPrecos(textWord):
    _str = re.sub('[^a-zA-Z0-9-_.]', '', textWord)
    # Check if selected word matches short forms[LHS] in text file.
    if _str.upper() in abbrRemov.keys():
        # If match found replace it with its appropriate phrase in text file.
        _str = abbrRemov[_str.upper()];
    _str = stem.stem(_str)
    _str = lmtz.lemmatize(_str, 'v')
    return _str

def tweets_to_clusters(inputfile,clustersFile):
    x = pd.read_csv(inputfile,',')
    print(x['text'])

    y = pd.read_csv(clustersFile,',')
    print(y["tweetd"])

    tweets = {}
    merged = pd.merge(y, x, left_on='tweetd', right_on='id')

    col = ['tweets', 'clusterID']
    df = pd.DataFrame(columns=col, index=None)
    df['tweets'] = merged['text']
    df['clusterID'] = merged['clusterno']
    df.to_csv('../MyOutputs/clusters.csv')



"""""
class purpose: general cluster class clustering
author: Shafaq Arshad
"""
keysToMatch = {'N', '^', 'Z', 'M', '#', 'V', 'T', 'U'}
class cluster:
    def __init__(self, cno):
        self.cno = cno
        self.ids = []
        self.text = {}  # cocantated tweets that has already passed through NER(named entity recogniser)
        self.retweetMap=[]
    # function add a tweet to unit cluster
    def addClusterId(self, id, text):
        self.ids.append(id)
        for key in text:
            if key in self.text:
                self.text[key] = self.text[key] | text[key]
            else:
                #print(text[key])
                self.text[key] = text[key]
                #print(self.text[key])

    def extendReweetMap(self,retweets):
        self.retweetMap.extend(retweets)

    # determine if cluster is full
    def IsClusterFull(self):
        return (len(self.ids) == 3);

    # return list of tweetid's in cluster
    def getTweetid(self):
        return self.ids

    """""""""""
    this function comutes the similarity score for two tweets text strings tweeta & tweetb
    returb a float value for similarity score
    input: two strings representing tweets to compare

    """""""""""

    def similarity(self, cluster2,id):

        # # # matching links. If a links matches return a infity score as if they havr same link they talk abut same event
        # key = 'U'
        # if (key in cluster2.keys() and key in self.text.keys()):
        #     setus = cluster2[key] & self.text['U']
        #     if len(list(setus.elements())) != 0:
        #         SimilrityScore = numpy.math.inf
        #         return (self.cno,SimilrityScore)
        # N=Commen Noun ^= Proper noun Z = Propernoun +posessive, V is verb #hastag

        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2:
                a1 = cluster2[k]
                b1 = self.text[k]
                a2 = a1 & b1
                similarity[k] = len(a2)/len(a1)
            else:
                similarity[k] = 0

        SimilrityScore = (a * similarity['N']) + (b * similarity['^']) + (b * similarity['Z']) + (
                c * similarity['V']) + (d * similarity['#'])
        #print(len(cluster2))
        return (self.cno,SimilrityScore)


class MergeCluster(cluster):
    def Extend(self, cluster):
        self.ids.extend(cluster.ids)
        for key in cluster.text:
            if key in self.text:
                self.text[key] = self.text[key] | cluster.text[key]
            else:
                self.text[key] = cluster.text[key]

    def similarity(self, cluster2):

        key = 'U'
        if (key in cluster2.text.keys() and key in self.text.keys()):
            setus=cluster2.text[key]& self.text['U']
            if len(list(setus.elements())) != 0:
                 SimilrityScore = numpy.math.inf
                 return (self.cno,SimilrityScore)
        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2.text:
                a1 = cluster2.text[k]
                b1 = self.text[k]
                a2 = a1 & b1
                similarity[k] = sum(a2.values())/sum(a1.values())
            else:
                similarity[k] = 0

        SimilrityScore = ((a * similarity['N']) + (b * similarity['^']) + (b * similarity['Z']) + (
                c * similarity['V']) + (
                                 d * similarity['#']))
        return (self.cno,SimilrityScore)

def takeSecond(elem):
    return elem[1]
def NERPass(text):
    Preprocessed =defaultdict()
    java_object = gateway.entry_point.getStack(text.lower())  # return {A: "adjective list",N:"nouns list....}
    keysToMatch = {'N', '^', 'Z', 'M', '#', 'V', 'T'}
    if 'U' in java_object:
        Preprocessed['U'] = mset(lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object['U']))
    for key in keysToMatch:
        if(key in java_object):
         Preprocessed[key]=mset(lmtz.lemmatize(word,'v') for word in re.split(" ", java_object[key]))
    return Preprocessed

"""""
this takes a cluster compare it to merge cache if a similar mergeunit is found 
we extend that mergeunit by adding this cluster
"""


def MergeClusters(unitCluster):
    score = []
    if len(MergeCache) == 0:
        cno1 = len(MergeCache)
        MergeCache[cno1] = MergeCluster(cno1)
        MergeCache[cno1].Extend(unitCluster)
        return
    score = list(map(lambda x: MergeCache[x].similarity(unitCluster),MergeCache.keys()))
    score = sorted(score, key=takeSecond, reverse=True)
    #print(score)   # print("score"+str(score[0]))
    if (score[0][1] > threshold2):
        MergeCache[score[0][0]].Extend(unitCluster)
    else:
        cno1 = len(MergeCache)
        MergeCache[cno1] = MergeCluster(cno1)
        MergeCache[cno1].Extend(unitCluster)
    #print('merged')

import os

"""""""""
Alltweet is a pd dataframe
id|text|username|timestamp
  |    |        |       

"""""""""


def theLastMerge():
    k=1
    lenght=len(MergeCache)
    deactivated=[]
    for i in range(len(MergeCache)):
      score=[]
      for cluster in MergeCache:
          if(cluster not in deactivated and cluster != i):
              scorr=MergeCache[cluster].similarity(MergeCache[i])
              if (scorr[1]> .8):
                  MergeCache[cluster].Extend(MergeCache[i])
                  deactivated.append(i)
                  break
              else:
                  score.append(scorr)
      if( i not in deactivated):
          score = sorted(score, key=takeSecond, reverse=True)
          if (score[0][1] > threshold3):
              MergeCache[score[0][0]].Extend(MergeCache[i])
              deactivated.append(i)
    for cluster in MergeCache:
        if cluster not in deactivated:
            for td in MergeCache[cluster].ids:
                writer.writerow({'clusterno': MergeCache[cluster].cno, 'tweetd': td})

def myFun(x,java_object,r):
    return x.similarity(java_object,r)
def myFun3(x):
    return x
if __name__ == '__main__':
    print("processing data: Thresholds are "+str(threshold)+" and "+str(threshold2))
    MergeCache = defaultdict(MergeCluster)
    time1=time.time()
    #Lenths_Dic={}
    Alltweets['text'] = Alltweets['text'].apply(lambda x: ' '.join([translator(word) for word in x.split()]))
    Alltweets['text']= Alltweets['text'].apply(lambda x: NERPass(x.lower()))
    print("proceesed data and staring clustering ")
    UntiClusters = defaultdict(cluster)
    #i = 0;
    cno=-1
    # for each tweet incoming
    for row in Alltweets.itertuples():
        java_object = row.text

        if len(UntiClusters) != 0:  # precation incase no unitclust in cache

            avg=list(map(lambda x: myFun(UntiClusters[x],java_object,row.id),UntiClusters.keys()))
            avg = sorted(avg,key= lambda x: x[1], reverse=True)
# sorted(avg, key=takeSecond, reverse=True)
            if threshold < avg[0][1]:  # if threshold is passed add it to the cluster
                UntiClusters[avg[0][0]].addClusterId(row.id, java_object)
                if UntiClusters[avg[0][0]].IsClusterFull():
                    MergeClusters(UntiClusters[avg[0][0]])
                    UntiClusters.pop(avg[0][0])

            else:  # make a new one
                cno +=1
                UntiClusters[cno] = cluster(cno=cno)
                UntiClusters[cno].addClusterId(id=row.id, text=java_object)

        else:
            cno +=1
            UntiClusters[cno] = cluster(cno=cno)
            UntiClusters[cno].addClusterId(id=row.id, text=java_object)
    print("hel")
            # ----------------------------------------------------------------------
    for cluster in UntiClusters:
        MergeClusters(UntiClusters[cluster])

    theLastMerge()


    t2=time.time()
    print("time to cluster "+str(time.time()-time1))

    tweets_to_clusters(inputFile,Outfilename)
    Tagger = TopicCategorization()
    Tagger.tagging()
    t2 = time.time()
    print("time to summarize " + str(time.time() - time1))
