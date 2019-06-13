from DatasetA.EventDetection.DynammicClustering import DynammicClustering

clusteringAlg = DynammicClustering(a=float(5 / 11), b=float(0 / 11),
                                   c=float(1 / 11), d=float(5 / 11), threshold=0.1, threshold2=0.2, threshold3=.5,
                                   inputFile="../Data/mytweet15 May.csv", Outfilename="../MyOutputs/clustersIds.csv")

print(clusteringAlg.NERPass("hey I am shafaq ;p;p whats up? wth",0))