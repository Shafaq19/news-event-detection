import csv
import re

import pandas
from collections import defaultdict

from pip._internal.commands.list import tabulate
from py4j.java_gateway import JavaGateway
import matplotlib.pyplot as plt
import numpy
from collections import Counter as mset
import scipy.cluster.hierarchy as hcluster
from sklearn.metrics import adjusted_rand_score, fowlkes_mallows_score, jaccard_similarity_score


"""""""""""""""""""""
similarity score parameters a,b,c,d
"""""""""""""""""""""

a = .75#commen Noun
b = 2.0#properNoun
c = .45#verb
d = 2#hashtag threshold
threshold = 5
threshold2 =18

gateway = JavaGateway()  # connect to the JVM
Alltweets = pandas.read_csv("mytweet2", ",")
filename = "clusters4.csv"
output = open(filename, mode='w', encoding='utf-8')
fieldnames = ['clusterno', 'tweetd']
writer = csv.DictWriter(output, fieldnames=fieldnames)

writer.writeheader()


"""""
class purpose: general cluster class clustering
author: Shafaq Arshad
"""
class cluster:
    def __init__(self, cno):
        self.cno = cno
        self.ids = []
        self.text={}#cocantated tweets that have already passed through NER(named entity recogniser)
    #function add a tweet to unit cluster
    def addClusterId(self,id, text):
        self.ids.append(id)
        for key in text:
            if key in self.text:
                self.text[key] += " "
                self.text[key]+=text[key]
            else:
                self.text[key]=text[key]

    #determine if cluster is full
    def IsClusterFull(self):
        return (len(self.ids)==3);

    #return list of tweetid's in cluster
    def getTweetid(self):
        return self.ids

    """""""""""
    this function comutes the similarity score for two tweets text strings tweeta & tweetb
    returb a float value for similarity score
    input: two strings representing tweets to compare

    """""""""""

    def similarity(self,cluster2):
        #matching links. If a links matches return a infity score as if they havr same link they talk abut same event
        if(('U' in cluster2 and cluster2['U'] is not None) and 'U' in self.text):
            u=re.split(" ", cluster2['U'])
            # N=Commen Noun ^= Proper noun Z = Propernoun +posessive, V is verb #hastag
            for url in u:
                if url in self.text['U']:
                    SimilrityScore = numpy.math.inf
                    return SimilrityScore
        # N=Commen Noun ^= Proper noun Z = Propernoun +posessive, V is verb #hastag
        keysToMatch = {'N', '^', 'Z', 'M', '#', 'V', 'T'}
        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2:
                a1 = mset(re.split(" ", cluster2[k]))
                b1 = mset(re.split(" ", self.text[k]))
                a1 = a1 & b1
                similarity[k] = len(list(a1.elements()))
            else:
                similarity[k] = 0
        SimilrityScore = (a * similarity['N']) + (b * similarity['^']) + (b * similarity['Z']) + (
                    c * similarity['V']) + (
                                 d * similarity['#'])
        return SimilrityScore

class MergeCluster(cluster):
    def Extend(self,cluster):
        self.ids.extend(cluster.ids)

        for key in cluster.text:
            if key in self.text:
                self.text[key] +=" "
                self.text[key]+=cluster.text[key]
            else:
                self.text[key] = cluster.text[key]

    def similarity(self, cluster2):
        key='U'
        if (key in cluster2.text.keys() and key in self.text.keys()):
            u = re.split(" ", cluster2.text['U'])
            # N=Commen Noun ^= Proper noun Z = Propernoun +posessive, V is verb #hastag
            for url in u:
                if url in self.text['U']:
                    SimilrityScore = numpy.math.inf
                    return SimilrityScore

        keysToMatch = {'N', '^', 'Z', 'M', '#', 'V', 'T'}
        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2.text:
                a1 = mset(re.split(" ", cluster2.text[k]))
                b1 = mset(re.split(" ", self.text[k]))
                a1 = a1 & b1
                similarity[k] = len(list(a1.elements()))
            else:
                similarity[k] = 0
        SimilrityScore = (a * similarity['N']) + (b * similarity['^']) + (b * similarity['Z']) + (
                c * similarity['V']) + (
                                 d * similarity['#'])
        return SimilrityScore



MergeCache = defaultdict(MergeCluster)




def takeSecond(elem):
    return elem[1]





"""""
this takes a cluster compare it to merge cache if a similar mergeunit is found 
we extend that mergeunit by adding this cluster
"""
def MergeClusters(unitCluster):
    score = []
    if len(MergeCache) == 0:
        cno=len(MergeCache)
        MergeCache[cno]=MergeCluster(cno)
        MergeCache[cno].Extend(unitCluster)
        return

    for cluster in MergeCache:
        merge = ""
        score.append((cluster,MergeCache[cluster].similarity(unitCluster)))

    score = sorted(score, key=takeSecond, reverse=True)
    print("Score in the Merge Cluster")
    print(score[0])
    if (score[0][1] > threshold2):
        MergeCache[score[0][0]].Extend(unitCluster)
    else:
        cno=len(MergeCache)
        MergeCache[cno]=MergeCluster(cno)
        MergeCache[cno].Extend(unitCluster)

import os
"""""""""
Alltweet is a pandas dataframe
id|text|username|timestamp
  |    |        |       
  
"""""""""
if __name__ == '__main__':
    UntiClusters = defaultdict(cluster)
    i = 0;
    #for each tweet incoming
    for row in Alltweets.itertuples():
        java_object = gateway.entry_point.getStack(row.text)# return {A: "adjective list",N:"nouns list....
        if (i != 20000):#checking for 2000 tweets
            if len(UntiClusters) != 0:#precation incase no unitclust in cache
                avg = []
                for ucluster in UntiClusters:
                    avg.append((ucluster, UntiClusters[ucluster].similarity(java_object)))#compare the tweet to all clusters

                avg = sorted(avg, key=takeSecond, reverse=True)
                if threshold < avg[0][1]:#if threshold is passed add it to the cluster
                    UntiClusters[avg[0][0]].addClusterId(row.id,java_object)
                    if UntiClusters[avg[0][0]].IsClusterFull():
                        MergeClusters(UntiClusters[avg[0][0]])
                        UntiClusters.pop(avg[0][0])

                else:#make a new one
                    cno = len(UntiClusters)
                    UntiClusters[cno] = cluster(cno=len(UntiClusters))
                    UntiClusters[cno].addClusterId(id=row.id, text=java_object)

            else:
                cno=len(UntiClusters)
                UntiClusters[cno]=cluster(cno=len(UntiClusters))

                UntiClusters[cno].addClusterId(id=row.id,text=java_object)

            i += 1

            # ----------------------------------------------------------------------
        else:
            break
    for cluster in UntiClusters:
        MergeClusters(UntiClusters[cluster])
    for cluster in MergeCache:
        for td in MergeCache[cluster].getTweetid():
            writer.writerow({'clusterno': MergeCache[cluster].cno, 'tweetd': td })


