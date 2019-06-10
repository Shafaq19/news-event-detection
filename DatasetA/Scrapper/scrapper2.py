import csv

import math
import tweepy
from pandas import read_csv

"""""
crawls the api for tweets 
args: user to crawl, nomber of tweets to fetch, the excel file to write the tweets too
tweet id, text,retweets, date formed will be saved in tweets.csv fie
"""
def crawl(user,count,writer):
    tweets=[]
    try:
        api = tweepy.API(auth)
        for status in tweepy.Cursor(api.user_timeline, id=user, retweets=True).items(count):
            tweet = status._json
            writer.writerow({'id': tweet['id'], 'created_at': tweet['created_at'], 'text': tweet['text'],
                             'user': tweet['user']['screen_name'], 'retweet_count': tweet['retweet_count']})
            tweets.append(tweet['text'])
    except Exception as e:
        print(e)
    return tweets

""""
function that look up tweets from the api from a list 
of users

"""""
def lookup_tweets(tweet_IDs, api):
    f=open('../Data/mytweet02.csv', 'wt', encoding="utf8")
    fieldnames = ['id', 'created_at', 'text', 'user', 'retweet_count']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    full_tweets = []
    tweet_count = len(tweet_IDs)
    print(tweet_count)
    no_of_lists = math.ceil(len(tweet_IDs) / 100)
    try:

        for i in range(no_of_lists):
            if len(tweet_IDs) < 100:
                results=api.statuses_lookup(id_=tweet_IDs[:],include_entities=False,trim_user=False)
                for tweet1 in results:
                    tweet = tweet1._json
                    writer.writerow({'id': tweet['id'], 'created_at': tweet['created_at'], 'text': tweet['text'],
                                     'user': tweet['user']['screen_name'], 'retweet_count': tweet['retweet_count']})

            else:
                results=api.statuses_lookup(tweet_IDs[:100],include_entities=False,trim_user=False)
                for tweet1 in results:
                    tweet = tweet1._json
                    writer.writerow({'id': tweet['id'], 'created_at': tweet['created_at'], 'text': tweet['text'],
                                     'user': tweet['user']['screen_name'], 'retweet_count': tweet['retweet_count']})
                tweet_IDs=tweet_IDs[100:]

        print("done")
    except tweepy.TweepError:
        print( 'Something went wrong, quitting...')
        #print(tweepy.TweepError.reason)
"""""
token initialization for api
"""""
access_key = '911986131230654464-Mv4djQ3PTcCW3cvDYxcFkZLGjj7kX7n'
access_secret = 'vDEEfyUESHqsHtZGvhgUTddCjWdchlNq2UfWZBlN3Jl9M'
consumer_key = 'VtCTykihYAXXvX4sV3CVsdLM9'
consumer_secret = 'jPIKHNM8F4XoLwTrHdbSWBlzCJb3AzxOF3WLm75Hf6dwyZEYm9'
try:
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify= True)
    print("doen authenticaing")
except:
    print("\nError in authenticating with the Twitter's API")
    exit()


"""""
Main scrapper fetches tweets and saves it
"""
def scrapp():

    users=['BBCBreaking','nytimes','Reuters','ABCWorldNewsNow','BBCWorld','BreakingNews','FoxNews','MSNBC','NBCNews','SkyNews','CNN','geonews_english']
    f=open('../Data/mytweet02.csv', 'wt', encoding="utf8")
    fieldnames = ['id', 'created_at', 'text', 'user', 'retweet_count']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for user in users:
        crawl(user,500,writer)
