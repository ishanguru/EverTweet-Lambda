from flask import Flask
import tweepy
import json
import time
import ConfigParser
import tweepy
from tweepy.streaming import StreamListener
import os

config_file_path = os.environ['LAMBDA_TASK_ROOT'] + '/configurations.txt'

config = ConfigParser.ConfigParser()
config.readfp(open(config_file_path))

consumerKey=config.get('API Keys', 'consumerKey')
consumerSecret=config.get('API Keys', 'consumerSecret')
accessToken=config.get('API Keys', 'accessToken')
accessSecret=config.get('API Keys', 'accessSecret')

def tweet_lambda_handler(event, context):
    print('This is the event:')
    print(event)
    print('This is the context:')
    print(context)

    username = event['username']
    print username

    user_tweets = get_tweets(username)

    return user_tweets

def get_tweets(username):

    auth = tweepy.AppAuthHandler(consumerKey, consumerSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    timeline = api.user_timeline(screen_name=username, count=3200)
    user_tweets = []

    for current_tweet in timeline:
        if not current_tweet.retweeted:
            tweet = {}
            tweet['tweetId'] = current_tweet.id
            tweet['message'] = current_tweet.text
            tweet['author'] = current_tweet.user.name
            tweet['timestamp'] = current_tweet.created_at
            user_tweets.append(tweet)

    return user_tweets
