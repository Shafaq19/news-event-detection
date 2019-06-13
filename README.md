
Dataset Cittation:
Andrew J. McMinn, Yashar Moshfeghi, Joemon M. Jose. Building a large-scale 
corpus for Evaluating Event Detection on Twitter - Proceedings of the 22nd ACM
international conference on Conference on information & knowledge management.

similarity function taken from paper:
Liu, Xiaomo, Quanzhi Li, Armineh Nourbakhsh, Rui Fang, Merine Thomas, Kajsa Anderson, RussKociuba, et al. 2016.
“Reuters Tracer: A Large Scale System of Detecting and Verifying Real-Time News Events from Twitter.” in the Proceedings
of the 25th ACM International Conference on Information and Knowledge Management, 207–216, Indianapolis, Indiana, October 24–28.



To run this code:
Step1: Clone/download the Java code for NER from the repository:
git clone https://shafaqA15@bitbucket.org/shafaqA15/named-entity-recognizer.git
and run the java gateway
Step2: run the cluster_take2.py file that will generate clusters of tweets using the dynammic clustering algorithmin the foloowing two pharses:
    Unit Cluster:
    for incoming tweets:
        compare it to all unit clusters in cache
        find the cluster with max similarity score
        if that score is above the threshold:
            add the tweet to that cluster
            if cluster size is now 3  go to merge phase
        else
            form a new unit cluster

    if there are unit clusters now matched  with a merge cluster:
        merge them too

Merge Pharse:
    for incoming cluster:
        add it to the most similar merge cluster if score above a threshold
        else make a new merge cluster


Step3 : evaluation:
        evaluate clusters using RandIndex, Recall




