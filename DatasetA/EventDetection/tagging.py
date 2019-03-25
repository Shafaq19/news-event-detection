import csv
import json
import re

import pandas
import requests

from DatasetA.EventDetection.index import summarization

calais_url = 'https://api.thomsonreuters.com/permid/calais'
# File path which consists of Abbreviations.
fileName = "../utils/slang.txt"#
#  File Access mode [Read Mode]
accessMode = "r"
abbrRemov={}
with open(fileName, accessMode) as m:
    dataFromFile = csv.reader(m, delimiter="=")
    #print(dataFromFile)
    for row in dataFromFile:
        abbrRemov[row[0]]=row[1]
""""""""""""""""
preproceessing variable and functions
"""""


def translator(user_string):
    # Check if selected word matches short forms[LHS] in text file.
    if user_string.upper() in abbrRemov.keys():
        # If match found replace it with its appropriate phrase in text file.
        user_string = abbrRemov[user_string.upper()];
    return user_string

# #crawl or fetch the tweets max: 3200
# T.crawl()

def parseFile(input_data,headers):
    response = requests.post(calais_url, data=input_data, headers=headers, timeout=80)
    print('status code: %s' % response.status_code)

    content = json.loads(response.text)
    for keys in content:
        if "_typeGroup" in content[keys]:
            if content[keys].get("_typeGroup")=='topics':
                topic=content[keys].get("name")
                return topic
    return "No topic found"


def tweet_clean(t):
		t = re.sub(
		r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
		" ", t)
		t = t.replace("#", "")
		t = t.replace("@", "")
		t = re.sub(r"[^\w\s]","",t)
		t = re.sub(" \d+", " ", t)

		return t
""""""""""""""""
preproceessing variable and functions
"""""


def translator(user_string):
    # Check if selected word matches short forms[LHS] in text file.
    if user_string.upper() in abbrRemov.keys():
        # If match found replace it with its appropriate phrase in text file.
        user_string = abbrRemov[user_string.upper()];
    return  tweet_clean(user_string)
    #return user_string

if __name__ == "__main__":
    access_token = "EB2iLsNMLNGUCMsiQo1F7Gg3fKDNDuZs";
    headers = {'X-AG-Access-Token': access_token, 'Content-Type': 'text/raw', 'outputformat': 'application/json'}
    clusterFile='../MyOutputs/clusters.csv'
    df = pandas.read_csv(clusterFile).drop(['Unnamed: 0'], axis=1)
    groups = df.groupby('clusterID')

    filename = "../MyOutputs/topics.csv"
    output = open(filename, mode='w', encoding='utf-8')
    fieldnames = ['clusterno', 'topic', 'tweet']
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    summ = summarization(clusterFile)
    count=0
    for name, group in groups:
        if count < 1000:
            tweety = ' '.join(group['tweets'].tolist())
            tweety=translator(tweety)
            topic=parseFile(tweety, headers)
            tweet=summ.loc[summ ['cluster no'] == name,['tweet']].tweet
            if len(tweet)!=0:
                writer.writerow({'clusterno': name, 'topic': topic,'tweet': tweet})
        else:
            break