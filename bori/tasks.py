from __future__ import absolute_import, unicode_literals

import time

from .twitter_feed import twitter_feeder
import logging
import sys
import feedparser


import json

from .NewsFinder import NewsFinder
from celery import shared_task
from .twitter_reader import TwitterReader


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


@shared_task()
def my_print():
    print('hello world')
    
    
@shared_task(name='tasks.find_news')
def find_news(json_data):
    
    print('my_task')
    
    user_name = json_data['screenName']
   
    twt_number = 2
    twitter_reader = TwitterReader(twt_number)
    news_finder = NewsFinder()
    
    user_tweets = twitter_reader.read_user_tweet(user_name)
    news_list = news_finder.find_most_sim_news(user_tweets)
    news_dict = make_json_array(news_list)
    
    return news_dict

@shared_task(name='tasks.read_tweets')
def read_tweets(user):
    twt_number = 2
    twitter_reader = TwitterReader(twt_number)
    user_tweets = twitter_reader.read_user_tweet(user)
    
    return user_tweets
    
@shared_task(name='tasks.get_news_list')
def get_news_list(user_tweets):
    news_finder = NewsFinder()
    news_list = news_finder.find_most_sim_news(user_tweets)
    
    return news_list

@shared_task(name='tasks.get_headline_news_list')
def get_headline_news_list():
    url = 'https://news.google.com/news/rss/?hl=ko&gl=KR&ned=kr'
    news = feedparser.parse(url)
    
    return news

def make_json_array(news_list):
    news_dict = {}
    one_list =[]

    for news_info in news_list:
        for news in news_info:
            one_list.append(news)

    news_dict['news_list'] = one_list

    return news_dict



