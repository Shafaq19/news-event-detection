import csv

import math
import tweepy
from pandas import read_csv


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
"""""
  if (tweet['retweet_count']>0):
                        retweetMap = {}
                        retweet = api.retweets(tweet['id'], 5)
                        print(retweet)

**/
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
#
# tweetIdsFiles="tweets.csv"
# df=read_csv(tweetIdsFiles,",",header=None,index_col=None)
# print(df)
#
# tweet_ids_list = df[0].iloc[124510:].tolist()
#
# # results=lookup_tweets(tweet_ids_list,api)
#
users=['RadioPakistan','geonews_english','BBCBreaking','ARYNEWSOFFICIAL','nytimes','Reuters','ABCWorldNewsNow','BBCWorld','BreakingNews','FoxNews','MSNBC','NBCNews','SkyNews','CNN']
f=open('../Data/mytweet02.csv', 'wt', encoding="utf8")
fieldnames = ['id', 'created_at', 'text', 'user', 'retweet_count']
writer = csv.DictWriter(f, fieldnames=fieldnames)

writer.writeheader()
for user in users:
    t=crawl(user,500,writer)
    print(len(t))