from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from .NewsFinder import NewsFinder, TwitterReader
import json
import jpype

@csrf_exempt
def hello(request):
    jpype.attachThreadToJVM()
    print('#########hello view ####################')

    json_data = json.loads(request.body.decode('utf-8'))
    user = json_data['screenName']
    print(user)
    twitter_reader = TwitterReader()
    news_finder = NewsFinder()
    user_tweets = twitter_reader.read_user_tweet(user)
    news_list = news_finder.find_most_sim(user_tweets)
    news_dict = make_json_array(news_list)

    return JsonResponse(news_dict)



def make_json_array(news_list):
    news_dict = {}
    one_list =[]

    for news_info in news_list:
        for news in news_info:
            one_list.append(news)

    news_dict['news_list'] = one_list

    return news_dict



