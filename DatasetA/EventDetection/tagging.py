import csv
import json
import re

import pandas
import requests
import time

from DatasetA.EventDetection.index import summarization
class TopicCategorization:
    calais_url = 'https://api.thomsonreuters.com/permid/calais'
    abbrRemov={}

    def __init__(self):
        #  File path which consists of Abbreviations.
        fileName = "../utils/slang.txt"  #
        #  File Access mode [Read Mode]
        accessMode = "r"

        with open(fileName, accessMode) as m:
            dataFromFile = csv.reader(m, delimiter="=")
            # print(dataFromFile)
            for row in dataFromFile:
                 TopicCategorization.abbrRemov[row[0]] = row[1]

   # #crawl or fetch the tweets max: 3200
    # T.crawl()

    def parseFile(self,input_data, headers):
        status=False

        try:
            response = requests.post(TopicCategorization.calais_url, data=input_data.encode("utf-8"), headers=headers, timeout=80, )
        except:
                print("status code 200")

        if response.status_code == 200:
            content = json.loads(response.text)
            for keys in content:
                if "_typeGroup" in content[keys]:
                    if content[keys].get("_typeGroup") == 'topics':
                        topic = content[keys].get("name")
                        return topic

        return "No topic found"

    def translator(self,user_string):
        # Check if selected word matches short forms[LHS] in text file.
        if user_string.upper() in  TopicCategorization.abbrRemov.keys():
            # If match found replace it with its appropriate phrase in text file.
            user_string = TopicCategorization.abbrRemov[user_string.upper()];
        return user_string

    """"""""""""""""
    preproceessing variable and functions
    """""
    def tweet_clean(self,t):
        t = re.sub(
            r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
            " ", t)
        t = t.replace("#", "")
        t = t.replace("@", "")
        t = re.sub(r"[^\w\s]", "", t)
        t = re.sub(" \d+", " ", t)

        return t

    """"""""""""""""
    preproceessing variable and functions
    """""

    def translator(self,user_string):
        # Check if selected word matches short forms[LHS] in text file.
        if user_string.upper() in TopicCategorization.abbrRemov.keys():
            # If match found replace it with its appropriate phrase in text file.
            user_string = TopicCategorization.abbrRemov[user_string.upper()];
        return self.tweet_clean(user_string)

    def tagging(self,):
        access_token = "EB2iLsNMLNGUCMsiQo1F7Gg3fKDNDuZs";
        headers = {'X-AG-Access-Token': access_token, 'Content-Type': 'text/raw', 'outputformat': 'application/json'}
        clusterFile = '../MyOutputs/clusters.csv'
        df = pandas.read_csv(clusterFile).drop(['Unnamed: 0'], axis=1)
        groups = df.groupby('clusterID')

        filename = "../MyOutputs/topics.csv"
        output = open(filename, mode='w', encoding='utf-8')
        fieldnames = ['clusterno', 'topic', 'tweet']
        writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        summ = summarization(clusterFile)
        count = 0
        for name, group in groups:
            if count < 10:
                tweety = ' '.join(group['tweets'].tolist())# ahprt text document by joins tweets in the cluster
                tweety = self.translator(tweety)
                topic = self.parseFile(tweety, headers)
                tweet = summ.loc[summ['cluster no'] == name, ['tweet']].values
                tweet = self.translator(str(tweet[0]))

                if len(tweet) != 0:
                    writer.writerow({'clusterno': name, 'topic': topic, 'tweet': tweet})
            else:
                break
            count += 1




