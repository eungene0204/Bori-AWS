import logging
import sys

import jpype
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .NewsFinder import NewsFinder
from .tasks import read_tweets
from .tasks import get_news_list
from .tasks import get_headline_news_list


import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

@csrf_exempt
def hello(request):
    
    jpype.attachThreadToJVM()
    logger.info('hello view')

    json_data = json.loads(request.body.decode('utf-8'))
    news_list = None
    news_dict = None
   
    #r = find_news.delay(json_data)
   
    user = json_data['screenName']
    logger.info("user name:%s", user)
    
    news_finder = NewsFinder()
    
    try:
        news_list = get_headline_news_list.delay()
        
    except get_headline_news_list.OperationalError as ex:
        logger.exception('Sending task raised: %r', ex)
        
    news_dict = make_json_array(news_list.wait())
    print(news_dict)
    
    return JsonResponse(news_dict)
    
    '''
    twt_number = 2
    twitter_reader = TwitterReader(twt_number)
    user_tweets = twitter_reader.read_user_tweet(user)
    
    news_finder = NewsFinder()
    news_list = news_finder.find_most_sim_news(user_tweets)
    
    news_dict = make_json_array(news_list)
    '''

    '''
     user_tweets = read_tweets.delay(user)
    
    if user_tweets.ready():
        news_list = get_news_list.delay(user_tweets.get())
    
    if news_list is not None and news_list.ready():
        news_dict = make_json_array(news_list)
   
    if news_dict is not None:
        return JsonResponse(news_dict)

    '''
    
   

def make_json_array(news_list):
    news_dict = {}
    one_list =[]

    for news_info in news_list:
        for news in news_info:
            one_list.append(news)

    news_dict['news_list'] = one_list

    return news_dict



