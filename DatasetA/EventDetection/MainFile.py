import time

from DatasetA.EventDetection.DynammicClustering import DynammicClustering
from  DatasetA.EventDetection.ClusterClass import cluster, MergeCluster
from DatasetA.EventDetection.tagging import TopicCategorization
# from DatasetA.Scrapper.scrapper2 import scrapp
if __name__ == '__main__':
    print("Scrapping Twitter")
    # scrapp()

    stime=time.time()
    clusteringAlg=DynammicClustering( a=float(1 / 11),b=float(5 / 11),
                                      c=float(1 / 11) ,d=float(4 / 11), threshold = 0.16,threshold2 = 0.23,threshold3=.4,
                                      inputFile="../Data/mytweet02.csv",Outfilename = "../MyOutputs/clustersIds.csv")
    print("before preprocessing")
    print(clusteringAlg.Alltweets['text'][0])# OMG__> OH MY GOD
    clusteringAlg.Alltweets['text'] =  clusteringAlg.Alltweets['text'].apply(lambda x: ' '.join([ clusteringAlg.translator(word) for word in x.split()]))
    clusteringAlg.Alltweets['text'] = clusteringAlg.Alltweets['text'].apply(lambda x: clusteringAlg.tweet_clean(x.lower()))
    clusteringAlg.Alltweets['text'] = clusteringAlg.Alltweets['text'].apply(lambda x: clusteringAlg.NERPass(x.lower()))
    print("after preprocessing")
    print(clusteringAlg.Alltweets['text'][0])
    clusteringAlg.Alltweets=clusteringAlg.Alltweets[1:]

    print("starting clustering.....")
    cno = -1
    # for each tweet incoming
    for row in clusteringAlg.Alltweets.itertuples():
        java_object = row.text
        if len(clusteringAlg.UntiClusters) != 0:  # precation incase no unitclust in cache

            avg = list(map(lambda x: clusteringAlg.mySimilarityFun(clusteringAlg.UntiClusters[x], java_object, row.id), clusteringAlg.UntiClusters.keys()))
            #(c;no, similarity dcore)
            avg = sorted(avg, key=lambda x: x[1], reverse=True)#sort based on score
            #sorted(avg, key=takeSecond, reverse=True)
            if clusteringAlg.threshold < avg[0][1]:  # if threshold is passed add it to the cluster
                clusteringAlg.UntiClusters[avg[0][0]].addClusterId(row.id, java_object)
                if clusteringAlg.UntiClusters[avg[0][0]].IsClusterFull():
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


    # ----------------------------------------------------------------------
    for cluster in clusteringAlg.UntiClusters:
        clusteringAlg.MergeClusters(clusteringAlg.UntiClusters[cluster])

    clusteringAlg.theLastMerge()#so many clusters being generated ---> reduce number of cluster in a elegant way
    end=-stime+time.time()
    print("time to cluster"+str(end))
    stime=end
    clusteringAlg.tweets_to_clusters(clusteringAlg.inputFile, clusteringAlg.clusterfile)
    Tagger = TopicCategorization()
    Tagger.tagging()
    print("time to summarize " + str(time.time() - end))

