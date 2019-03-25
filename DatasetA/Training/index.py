import pandas as pd
import re
from nltk.stem import PorterStemmer
import math

def tweets_to_clusters():

    x = pd.read_csv("mytweet2",)
    print(x['text'])

    y = pd.read_csv("clustersNew.csv",)
    print(y["tweetd"])

    tweets = {}

    for i in range(len(y["tweetd"])):
        for j in range(len(x['id'])):
            if y["tweetd"][i] == x['id'][j]:
                z = y['clusterno'][i]
                a = x['text'][j]
                tweets[a] = z
                print(i)

    x = []
    y = []
    for key, value in tweets.items():
        x.append(str(key))
        y.append((value))

    col = ['tweets','clusterID']
    df = pd.DataFrame(columns=col)
    df['tweets']=x
    df['clusterID']=y
    df.to_csv('out.csv')

def get_clusters_txt(x):
    cluster_tweets = []
    all_tweets = []
    prev_id = x['clusterID'][0]
    for i in range(len(x)):
        id = x['clusterID'][i]
        if id == prev_id:
            all_tweets.append(x['tweets'][i])
        else:
            prev_id = id
            cluster_tweets.append(all_tweets)
            all_tweets = []
            all_tweets.append(x['tweets'][i])
    return cluster_tweets

def get_stop_words_list(stop_words):
    with open('F:/BSCS-FAST/Semester 7/Informaiton Retrieval/assignments/assignments/learning/stoplist.txt') as stop_words_file:
        for line in stop_words_file:
            line = line.strip()
            stop_words.append(line)


def filter_ans_from_stop_words(ans, stop_words_filtered_list, stop_words):
    for token in ans:
        if not token in stop_words:
            stop_words_filtered_list.append(token)


def apply_stemming(stop_words_filtered_list):
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in stop_words_filtered_list]
    return stems


def tokenize_clusters(cluster_x_all):
    this_cluster_tokens = []
    for i in range(len(cluster_x_all)):
        tweet = cluster_x_all[i]
        tokens = tweet.split()

        this_tweet_tokens = []
        for token in tokens:
            result = re.match("\w+(\.?\w+)*", token)
            if result:
                if re.match("\w+(\.?\w+)*", token).group() == token:
                    this_tweet_tokens.append(token.lower())

        #stop_words = []
        #stop_words_filtered_list = []

        #get_stop_words_list(stop_words)
        #filter_ans_from_stop_words(this_tweet_tokens, stop_words_filtered_list, stop_words)

        #this_tweet_tokens_tokens = apply_stemming(stop_words_filtered_list)

        this_cluster_tokens.append(this_tweet_tokens)

    return this_cluster_tokens

def summarization():
    df = pd.read_csv('out.csv')

    cluster_tweets = get_clusters_txt(df)

    tokenized_clusters =[]
    final ={}

    # sending whole cluster one by one to get it tokens
    for i in range(len(cluster_tweets)):
        cluster_x_all  = cluster_tweets[i]
        tokenized_clusters.append(tokenize_clusters(cluster_x_all))

    #
    for i in range(len(tokenized_clusters)):
        x = tokenized_clusters[i]

        count = 0
        counts = {}
        p_count = 0

        y = []
        for j in range(len(x)):
            y = y + x[j]
        # calculating total worrds in each cluster.
        total_words = len(y)
        #this delets if a signle word in apperaing more then once in an array
        y = set(y)
        y = list(y)
        for j in range(len(y)):
            word = y[j]

            #count variable is used to count the no occuerances of a word in entire corpus
            #p_count varibale is used to count that a word has apperead in how many tweets/posts.
            for k in range(len(x)):
                for l in range(len(x[k])):
                    #counting number of occurences of each word in each tweet
                    if word == x[k][l]:
                        count += 1
                if word in x[k]:
                    #counting number of words in each tweets/posts
                    p_count += 1
            #counts contains both varibales count and p_counts
            #counts is a hash map
            #it is indexed by words which appeard in our corpus
            counts[word] = [count, p_count]
            count = 0
            p_count = 0

        final[i] = counts

        print(final[0])

    sum_tweets = []


    #this iterates for each cluster

    r = []
    t = []
    a = []
    for ind in range(len(tokenized_clusters)):

        # x reads the every cluster(in tokenized form) one by one
        x = tokenized_clusters[ind]
        y = []

        #this loop appends each tweet in a signle cluster to a single array
        #which is then used to calculaate the total number of words in a cluster
        for j in range(len(x)):
            y = y + x[j]

        total_words = len(y)

        #counts total posts in a singel cluster
        total_posts = len(tokenized_clusters[ind])

        cluster = final[ind]

        term_weights = []
        post_weights = []
        y = total_words
        z = total_posts

        # this inner loop interates for each tweet in a cluster
        for i in range(len(tokenized_clusters[ind])):
            post = tokenized_clusters[ind][i]

            # this loop iterates for each word in tweet, in that cluster
            # this loop calculates weight for each term in a tweet
            for k in range(len(post)):
                term = post[k]
                v = final[ind][term]
                tf = v[0]/y
                idf = z/v[1]
                term_weights.append(tf*math.log(idf, 2))

            # this calculates weight of a whole post
            post_weights.append(sum(term_weights)/(max(0.5, len(post))))
            term_weights = []

        # selects a term with highest weight
        i = post_weights.index(max(post_weights))
        post = (tokenized_clusters[ind][i])


        r.append(i)
        t.append(cluster_tweets[ind][i])
        a.append(ind)
        # it keeps the summarized tweet and its position in that cluster
        result = [i,cluster_tweets[ind][i]]
        # it keeps all the tweets selected as summary. An array of results vairable.
        sum_tweets.append(result)
        #
        # print(ind)
        # print(i)
        # print(post_weights)
        # print(cluster_tweets[ind][i])

    select_tweet = pd.DataFrame({'cluster no':a,'tweet id':r,'tweet':t})

    select_tweet.to_csv("../MyOutputs/summary.csv")
    return select_tweet