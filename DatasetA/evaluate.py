import csv
from collections import defaultdict

import os

import itertools

from pandas import read_csv

parent_folder = os.getcwd()
totaltweets=0

MergeCache={}# contains tweetid and assigned cluster
myclusters=[]
i=0
with open('t1_0.5t2_0.32.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
      myclusters.append(row['clusterno'])
      MergeCache[int(row['tweetd'])]=int(row['clusterno'])

path2="..\\Raw_Data\\CS\\events.tsv"
df=read_csv(path2,"\t",index_col=None)
eventclusters=  dict([(i,a) for i, a in zip(df.TweetID, df.EventID)])
print("No of evens: "+str(len(set(df['EventID'].tolist()))))
print("No of clusters: "+str(len(set(myclusters))))
TP=0
TN=0
FP=0
FN=0
tweetPairs= itertools.combinations(MergeCache,2)#get pairs of tweets
for pair in tweetPairs:
    tweet1=pair[0]
    tweet2= pair[1]
    if(eventclusters[tweet1]==eventclusters[tweet2]):#they are  similar
        if(MergeCache[tweet1]==MergeCache[tweet2]):# also they are clustered together its a TP
            TP+=1
        else:#similar but different ckusters assigned
            FN+=1
    else:#differnt class
        if (MergeCache[tweet1] == MergeCache[tweet2]):  # also they are clustered together FP
            FP += 1
        else:  # dismilar and different clusters assigned
            TN += 1
print("RAND INDEX "+str((TP+TN)/(TN+TP+FN+FP)))
print("Recall"+str(TP/(TP+FN)))