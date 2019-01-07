import pandas as pd
import gensim
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer
import numpy as np
np.random.seed(2018)
import nltk
from nltk import PorterStemmer
from pprint import pprint

#function for stemming
def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

#preprocessing function
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def implementLDA():
    #Reading data from csv file into dataframe
    data = pd.read_csv('out.csv', error_bad_lines=False)
    data_text = data[['tweets','clusterID']]
    documents = data_text

    #grouping data by same cluster IDs and consider it as a single document
    documents = documents.groupby('clusterID',as_index=False).agg(lambda x: x.tolist())
    documents['Joined'] = documents.tweets.apply(', '.join)
    documents.drop(documents.columns[1], axis=1, inplace=True)
    cols = documents.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    documents = documents[cols]

    print("Number of Clusters: ",len(documents))
    nltk.download('wordnet')

    #preprocessing
    processed_docs = documents['Joined'].map(preprocess)

    #making dictionary and bag of words from the tokens
    dictionary = gensim.corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=1, no_above=0.5, keep_n=100)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]

    #training the lda_model for topic filtering from the given tokens and clusters
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

    #reading the data again to test it on the trained model
    test_data = pd.read_csv('out.csv', error_bad_lines=False)
    test_tweets = test_data["tweets"].values

    hashTags = []
    #passing each tweet through model and save the highest weighted word as hashtag topic of that tweet
    for tweet in test_tweets:
        bow_vector = dictionary.doc2bow(preprocess(tweet))
        print("--------------------------------")
        for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1 * tup[1]):
            tag = "#"+lda_model.print_topic(index, 1)[7:-1]
            print(tag)
            hashTags.append(tag)
            break

    #writing data back to result.csv file in given format
    se = pd.Series(hashTags)
    test_data['Hashtag'] = se.values
    test_data.to_csv("result_LDA.csv",index=False)


