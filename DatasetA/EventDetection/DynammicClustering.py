import ast
import csv
import re
from collections import defaultdict

from collections import Counter as mset

import numpy
from nltk import WordNetLemmatizer
from py4j.java_gateway import JavaGateway
import pandas as pd
# File path which consists of Abbreviations.
from MainFolder.EventDetection.ClusterClass import MergeCluster,cluster

fileName = "../utils/slang.txt"#
#  File Access mode [Read Mode]
accessMode = "r"
abbrRemov={}
with open(fileName, accessMode) as m:
    dataFromFile = csv.reader(m, delimiter="=")
    #print(dataFromFile)
    for row in dataFromFile:
        abbrRemov[row[0]]=row[1]
class DynammicClustering:
    """""""""""""""
    Initializing NER model and files input
    """""""""""""""
    gateway = JavaGateway()  # connect to the JVM
    def __init__(self, a=float(1 / 11),b=float(5 / 11), c=float(1 / 11) ,d=float(4 / 11), threshold = 0.16,threshold2 = 0.3,threshold3=.4,inputFile="../Data/mytweet02.csv",Outfilename = "../MyOutputs/clustersIds.csv"):
        """""""""""""""""""""
        similarity score parameters a,b,c,d
        """""""""""""""""""""
        self.a = a # commen Noun
        self.b = b  # properNoun
        self.c = c  # verb
        self.d = d  # hashtag threshold
        self.threshold = threshold
        self.threshold2 = threshold2
        self.threshold3 = threshold3
        self.inputFile=inputFile
        self.clusterfile=Outfilename

        """""
        Inputfile reading
        """
        self.Alltweets = pd.read_csv(inputFile, ",")
        data = []
        data.insert(0,{'id':1234567890,'created_at': "Mon Apr 01 02:59:33 +0000 2019",'text':"@awesome_lucky Congrats to Mo Yan for being the 1st Chinese Nobel Prize of Literature laureate!",'user':"jakdaPk",'retweet_count': 5})

        self.Alltweets = pd.concat([pd.DataFrame(data), self.Alltweets], ignore_index=True,sort=False)
        output = open(Outfilename, mode='wt', encoding='utf-8')
        fieldnames = ['clusterno', 'tweetd']
        self.writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        self.writer.writeheader()

        output1 = open("../MyOutputs/slang2.csv", mode='wt', encoding='utf-8')
        fieldnames = ['id', 'slangs']
        self.slang_writer = csv.DictWriter(output1, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        self.slang_writer.writeheader()
        self.lmtz=WordNetLemmatizer()
        self.MergeCache = defaultdict(MergeCluster)
        self.UntiClusters = defaultdict(cluster)

    def mySimilarityFun(self,x, java_object, r):

        return x.similarity(java_object,r,self.a,self.b,self.c,self.d)

    def tweetPrecos(self,textWord):
            _str = re.sub('[^a-zA-Z0-9-_.]', '', textWord)
            # Check if selected word matches short forms[LHS] in text file.
            if _str.upper() in abbrRemov.keys():
                # If match found replace it with its appropriate phrase in text file.
                _str = abbrRemov[_str.upper()];
            return _str

    def tweets_to_clusters(self,inputfile, clustersFile):
            x = pd.read_csv(inputfile, ',')

            y = pd.read_csv(clustersFile, ',')
            z=pd.read_csv("../MyOutputs/slang2.csv",sep=',', quotechar='"',converters = {1: ast.literal_eval})

            tweets = {}
            merged = pd.merge(y, x, left_on='tweetd', right_on='id')
            merged=pd.merge(merged, z,left_on='id',right_on='id')
            col = ['tweets', 'clusterID']
            df = pd.DataFrame(columns=col, index=None)
            df['tweets'] = merged['text'].apply(
                lambda x: self.tweet_clean(x.lower(),merged.loc[merged['text']==x,'slangs'].iloc[0]))

            df['tweets'].replace('', numpy.nan, inplace=True)
            df.dropna(subset=['tweets'], inplace=True)
            df['clusterID'] = merged['clusterno']
            df.to_csv('../MyOutputs/clusters.csv')
            df['tweets'] = merged['text']
            df.to_csv('../MyOutputs/Cleaned.csv')
    #abbr removed
    def translator(self,user_string):
            # Check if selected word matches short forms[LHS] in text file.
            if user_string.upper() in abbrRemov.keys():
                # If match found replace it with its appropriate phrase in text file.
                user_string = abbrRemov[user_string.upper()];
            return user_string

    """"""""""""""""
      preproceessing variable and functions
      """""

    def tweet_clean(self, t,words):
        #cut out formating of new lines
        t=t.replace('\n'," ").replace('\r'," ")
        #for each word that we identified as removeable like emoji we remove it
        for ele in words:
             if len(ele) >= 2:
               t=t.replace(ele+" "," ")
        #remove mentions
        t = re.sub('@[^\s]+','',t)
        #remove urls
        t = re.sub(
            r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
            " ", t)
        #remove wspace
        t = re.sub(r"[^\w\s]", "", t)

        if (t.isspace()):
            return None

        return t
    """""
    
    performs Part of the speech tagging
    
    input: text to parse and tweet id
    out: Default dict of tags
    """
    def NERPass(self,text,id):
            Preprocessed = defaultdict()
            java_object = DynammicClustering.gateway.entry_point.getStack(text.lower())  # return {A: "adjective list",N:"nouns list....}
            keysToMatch = { '#', 'V', 'T'}
            nounKeys={'N', '^', 'Z', 'M','S'}
            removeables={'!','~','G','E','#'}
            slangs=[]
            if 'U' in java_object:
                #lematization does better preprocessing for more matches
                Preprocessed['U'] = mset(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object['U']))
            #match { '#', 'V', 'T'}
            for key in keysToMatch:
                if (key in java_object):
                    Preprocessed[key] = mset(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object[key]))
            sett=None
            #match Nouns (all kinds in here)
            for key in nounKeys:
                if (key in java_object):
                    if sett is None:
                        sett = mset(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object[key]))
                    else:
                        sett = sett |  mset(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object[key]))

            if sett != None:
                Preprocessed['N']=sett
            sett=None
            #slangs and emotican in the tweets
            for key in removeables:
                if (key in java_object):
                    if sett is None:
                        sett = set(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object[key]))
                    else:
                        sett = sett | set(self.lmtz.lemmatize(word, 'v') for word in re.split(" ", java_object[key]))

            if sett != None:
                self.slang_writer.writerow({'id': id, 'slangs': list(sett)})

            return Preprocessed

    def MergeClusters(self,unitCluster):
        score = []
        if len(self.MergeCache) == 0:
            cno1 = len(self.MergeCache)
            self.MergeCache[cno1] = MergeCluster(cno1)
            self.MergeCache[cno1].Extend(unitCluster)
            return
        score = list(map(lambda x: self.MergeCache[x].similarity(unitCluster,self.a,self.b,self.c,self.d), self.MergeCache.keys()))
        score = sorted(score, key=self.takeSecond, reverse=True)
        # print(score)   # print("score"+str(score[0]))
        if (score[0][1] > self.threshold2):
            self.MergeCache[score[0][0]].Extend(unitCluster)
        else:#new event
            cno1 = len(self.MergeCache)
            self.MergeCache[cno1] = MergeCluster(cno1)
            self.MergeCache[cno1].Extend(unitCluster)

    """""""""
    Alltweet is a pd dataframe
    id|text|username|timestamp
      |    |        |       
    
    """""""""

    def takeSecond(self,elem):
                return elem[1]
    def theLastMerge(self):
                # k = 1
                # lenght = len(self.MergeCache)
                # deactivated = []
                # for i in range(len(self.MergeCache)):
                #     score = []
                #     for cluster in range(i+1,len(self.MergeCache)):
                #         if (cluster not in deactivated and cluster != i):
                #             scorr = self.MergeCache[cluster].similarity(self.MergeCache[i],self.a,self.b,self.c,self.d)
                #             if (scorr[1] > .8):
                #                 self.MergeCache[cluster].Extend(self.MergeCache[i])
                #                 deactivated.append(i)
                #                 break
                #             else:
                #                 score.append(scorr)
                #     if (i not in deactivated):
                #         score = sorted(score, key=self.takeSecond, reverse=True)
                #         if (score[0][1] > self.threshold3):
                #             self.MergeCache[score[0][0]].Extend(self.MergeCache[i])
                #             deactivated.append(i)
                # xcnn=0
                # for cluster in self.MergeCache:
                #     if cluster not in deactivated:
                #         for td in self.MergeCache[cluster].ids:
                #             xcnn+=1
                #             self.writer.writerow({'clusterno': cluster, 'tweetd': td})
                for cluster in self.MergeCache:
                    for td in self.MergeCache[cluster].ids:
                            self.writer.writerow({'clusterno': cluster, 'tweetd': td})
