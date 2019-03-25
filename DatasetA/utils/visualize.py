import csv

import mpld3
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
# File path which consists of Abbreviations.
from sklearn.decomposition import PCA

fileName = "../utils/slang.txt"#
#  File Access mode [Read Mode]
accessMode = "r"
abbrRemov={}
with open(fileName, accessMode) as m:
    dataFromFile = csv.reader(m, delimiter="=")
    #print(dataFromFile)
    for row in dataFromFile:
        abbrRemov[row[0]]=row[1]
def translator(user_string):
    # Check if selected word matches short forms[LHS] in text file.
    if user_string.upper() in abbrRemov.keys():
        # If match found replace it with its appropriate phrase in text file.
        user_string = abbrRemov[user_string.upper()];
    return user_string

def preprocess(text):
    text = re.sub(r"http\S+", "", text)
    text=re.sub('@[^\s]+', '', text)
    text=' '.join([translator(word) for word in text.split()])
    return text
#define custom toolbar location
class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""
    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}
df = pd.read_csv('out1.csv')
df=df.loc[:1000]
df['tweets'] = df['tweets'].apply(lambda x: preprocess(x))
# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem.snowball import SnowballStemmer
synopsis=df['tweets'].values.tolist()

stemmer = SnowballStemmer("english")
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopsis:

    allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)
vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print( 'there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
print (vocab_frame.head())

from sklearn.feature_extraction.text import TfidfVectorizer
print(len(synopsis))
#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem)

tfidf_matrix = tfidf_vectorizer.fit_transform(synopsis) #fit the vectorizer to synopses

print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()
print(terms)
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

clusters = df['clusterID'].values.tolist()
print(df['clusterID'].value_counts())
import os  # for os.path.basename

import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS


# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
# mds = PCA(n_components=2)
#
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
print('j')
xs, ys = pos[:, 0], pos[:, 1]
#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
cluster_names = {0: 'Family, home, war',
                 1: 'Police, killed, murders',
                 2: 'Father, New York, brothers',
                 3: 'Dance, singing, love',
                 4: 'Killed, soldiers, captain'}

df2 = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=df['titles'].values.tolist(),tweet=synopsis))

# group by cluster
groups = df2.groupby('label')

# define custom css to format the font and to remove the axis labeling
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -200px;}
"""

# Plot
fig, ax = plt.subplots(figsize=(14, 6))  # set plot size
ax.margins(0.03)  # Optional, just adds 5% padding to the autoscaling

# iterate through groups to layer the plot
# note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18,
                     label=name, mec='none')
    ax.set_aspect('auto')
    labels = [i for i in group.tweet]
    # set tooltip using points, labels and the already defined 'css'
    tooltip = mpld3.plugins.PointLabelTooltip(points[0], labels,
                                             voffset=10, hoffset=10)
    # connect tooltip to fig
    mpld3.plugins.connect(fig, tooltip, TopToolbar())

    # set tick marks as blank
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])

    # set axis as blank
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
mpld3.plugins.connect(fig, tooltip)

mpld3.show()

ax.legend(numpoints=1)  # show legend with only one dot
plt.show()
mpld3.display()  # show the plot

# uncomment the below to export to html
# html = mpld3.fig_to_html(fig)
# print(html)
html = mpld3.fig_to_html(fig)
print(html)