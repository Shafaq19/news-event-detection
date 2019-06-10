import time

import numpy

from DatasetA.EventDetection.DynammicClustering import DynammicClustering
from  DatasetA.EventDetection.ClusterClass import cluster, MergeCluster
from DatasetA.EventDetection.tagging import TopicCategorization
# from DatasetA.Scrapper.scrapper2 import scrapp
from DatasetA.Scrapper.scrapper2 import scrapp

if __name__ == '__main__':
    print("Scrapping Twitter")
    #scrapp()
    stime=time.time()

    #initialize the algorithm
    clusteringAlg=DynammicClustering( a=float(5 / 11),b=float(0/ 11),
                                      c=float(1 / 11) ,d=float(5/ 11), threshold = 0.1,threshold2 = 0.2,threshold3=.5,
                                      inputFile="../Data/mytweet15 May.csv",Outfilename = "../MyOutputs/clustersIds.csv")
    print("before preprocessing")
    print(clusteringAlg.Alltweets['text'][0])# OMG__> OH MY GOD
    clusteringAlg.Alltweets['text'] = clusteringAlg.Alltweets['text'].apply(lambda x: clusteringAlg.NERPass(x.lower(),clusteringAlg.Alltweets.loc[clusteringAlg.Alltweets['text'] == x, 'id'].iloc[0]))
    print("after preprocessing")
    print(clusteringAlg.Alltweets['text'][0])
    clusteringAlg.Alltweets=clusteringAlg.Alltweets[1:]

    print("starting clustering.....")
    cno = -1
    # for each tweet incoming
    for row in clusteringAlg.Alltweets.itertuples():
        java_object = row.text
        if len(clusteringAlg.UntiClusters) != 0:  # precation incase no unitclust in cache

            #find similarty of the tweet to each cluster in the cache
            avg = list(map(lambda x: clusteringAlg.mySimilarityFun(clusteringAlg.UntiClusters[x], java_object, row.id), clusteringAlg.UntiClusters.keys()))

            avg = sorted(avg, key=lambda x: x[1], reverse=True)#sort based on score
            #see that if the most similar cluster matces above the threshold
            if clusteringAlg.threshold < avg[0][1]:  # if threshold is passed add it to the cluster
                clusteringAlg.UntiClusters[avg[0][0]].addClusterId(row.id, java_object)
                if clusteringAlg.UntiClusters[avg[0][0]].IsClusterFull():
                    #if cluster is fullgo to merge level
                    clusteringAlg.MergeClusters(clusteringAlg.UntiClusters[avg[0][0]])
                    clusteringAlg.UntiClusters.pop(avg[0][0])

            else:  # make a new one
                cno += 1
                clusteringAlg.UntiClusters[cno] = cluster(cno=cno)
                clusteringAlg.UntiClusters[cno].addClusterId(id=row.id, text=java_object)

        else:
            cno += 1
            clusteringAlg.UntiClusters[cno] = cluster(cno=cno)
            clusteringAlg.UntiClusters[cno].addClusterId(id=row.id, text=java_object)


    clusteringAlg.theLastMerge()#so many clusters being generated ---> reduce number of cluster in a elegant way
    end=-stime+time.time()
    print("time to cluster"+str(end))
    stime=end
    cleanned=clusteringAlg.tweets_to_clusters(clusteringAlg.inputFile, clusteringAlg.clusterfile)
    Tagger = TopicCategorization()
    Tagger.tagging()
    print("time to summarize " + str(time.time() - end))

