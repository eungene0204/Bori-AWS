from gensim.models import Word2Vec
from .word2vec_similarity import word2vec_similarity
from .twitter_feed import twitter_feeder
from .rss_parser import rss_parser
from .hangul_util import hangul_util

import pandas as pd
import os

class TwitterReader():
    
    def __init__(self):
        self.tweet_nummber = 3

    def read_user_tweet(self,user):

        tweet_feed = twitter_feeder()
        user_tweets = tweet_feed.get_user_timeline(user,self.tweet_nummber)

        return user_tweets

class NewsFinder():

    def __init__(self):
        print("~~~~~~~~~~~~~~~")
        self.module_dir = os.path.dirname(__file__)
        print("22222222222222222222")
        self.hangul_util = hangul_util()
        print("3333333333333333333")
        self.rss_parser = rss_parser()
        print("444444444444444444444")
        self.model, self.num_feature = self.load_model()
        print("55555555555555555555555555")

    def load_model(self):
        name = os.path.join(self.module_dir,'word2vec_model','word2vec_model_noun_20171013')
        model = Word2Vec.load(name)
        num_feature = 300

        return model, num_feature

    def read_objective_file(self):
        path = os.path.join(self.module_dir,'data','objective_words.csv')
        raw_words = pd.read_csv(path , header = 0, quoting=3, encoding='cp949',
                            error_bad_lines=False)
        values = raw_words.values;

        objective_words=[]
        for word in values:
             objective_words.append(word[0])

        return objective_words

    def find_most_sim(self,user_tweets):
        similarity_util = word2vec_similarity(self.model,self.num_feature)
        objective_words = self.read_objective_file()

        news_info_list = []
        for twt in user_tweets:
            try:
                twt = twt['text']
                twt = self.hangul_util.get_clean_hangul(twt)

                if(len(twt) <=0):
                    continue

                avg_vector = similarity_util.get_avg_vector(twt)
                similarity, category = \
                    similarity_util.find_most_similar_category(avg_vector,objective_words)

                print('#######################')
                print(twt)
                #print(self.model.most_similar([avg_vector]))
                #print(similarity)
                print(category)
                news = self.rss_parser.parse_feed(category)
               
                #can't find news
                print(len(news.entries))
                if(len(news.entries) == 0):
                    print('entrie is zero')
                    continue
                    
                news_info = self.rss_parser.get_news_info(news)
                news_info_list.append(news_info)

            except Exception as e:
                print(e)

        return news_info_list

