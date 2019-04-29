"""""
class purpose: general cluster class clustering
author: Shafaq Arshad
"""
import numpy

keysToMatch = {'N', '^', 'Z', 'M', '#', 'V', 'T', 'U'}
class cluster:
    def __init__(self, cno):
        self.cno = cno
        self.ids = []#tweet ids
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

    def similarity(self, cluster2,id,a,b,c,d):

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

    def similarity(self, cluster2,a,b,c,d):

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