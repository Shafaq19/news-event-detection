"""""
class purpose: general cluster class clustering
author: Shafaq Arshad
"""
import numpy
"""""

N: Noun
#: hastag

"""
keysToMatch = {'N', '#', 'V', 'U'}
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


        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2:
                a1 = cluster2[k]
                b1 = self.text[k]
                a2 = a1 & b1
                similarity[k] = len(a2)/len(a1)
            else:
                similarity[k] = 0

        SimilrityScore = (a* similarity['N']) + (
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
        similarity = {}
        for k in keysToMatch:
            if k in self.text and k in cluster2.text:
                a1 = cluster2.text[k]
                b1 = self.text[k]
                a2 = a1 & b1
                similarity[k] = sum(a2.values())/sum(a1.values())
            else:
                similarity[k] = 0
        similarity['U'] = numpy.math.inf if similarity['U'] > 0 else 0
        SimilrityScore = (a* similarity['N']) + (
                c * similarity['V']) + (d * similarity['#'])
        return (self.cno,SimilrityScore)