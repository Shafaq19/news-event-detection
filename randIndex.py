from collections import defaultdict

import os

import itertools
parent_folder = os.getcwd()
totaltweets=0
with open("clusters4.csv") as F:
    lines=F.readlines()
with open(parent_folder + "\\Raw_Data\\CS\\events.tsv") as F:
    lines1 = F.readlines()
MergeCache=defaultdict(list)# contains tweetid and assigned cluster
lines.pop(0)
lines.pop()
lines1.pop(0)
for line in lines:
    if(line)!="\n":
        line=line.split(',')
        totaltweets+=1;
        tweetId=line[1].split('\n')[0]
        MergeCache[tweetId]=line[0]
eventclusters = defaultdict(list)

for line in lines1:
        line=line.split('\t')
        eventclusters[line[1].split('\n')[0]]=line[0]# tweetid and class
TP=0
TN=0
FP=0
FN=0
tweetPairs= itertools.combinations(MergeCache,2)#get pairs of tweets
for pair in tweetPairs:
    if(eventclusters[pair[0]]==eventclusters[pair[1]]):#they are  similar
        if(MergeCache[pair[0]]==MergeCache[pair[1]]):# also they are clustered together its a TP
            TP+=1
        else:#similar but different ckusters assigned
            FN+=1
    else:#differnt class
        if (MergeCache[pair[0]] == MergeCache[pair[1]]):  # also they are clustered together FP
            FP += 1
        else:  # dismilar and different clusters assigned
            TN += 1
print("RAND INDEX "+str((TP+TN)/(TN+TP+FN+FP)))
print("Recall"+str(TP/(TP+FN)))