from gensim.models import Word2Vec
from .word2vec_similarity import word2vec_similarity
from .rss_parser import rss_parser
from .hangul_util import hangul_util
from multiprocessing import Pool

import pandas as pd
import os
import logging
import sys
import time
import multiprocessing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class NewsFinder():

    def __init__(self):
        self.module_dir = os.path.dirname(__file__)
        self.hangul_util = hangul_util()
        self.rss_parser = rss_parser()
        self.model, self.num_feature = self.load_model()

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

    def find_most_sim_news(self,user_tweets):
        
        mgr = multiprocessing.Manager()
    
        news_info_list = mgr.list()
        start_time = time.time()
        jobs = []
        
        
        for twt_json in user_tweets:
           
            try:
                twt = twt_json['text']

                logger.debug('User tweet:%s', twt)
                twt = self.hangul_util.get_clean_hangul(twt)
                
                #not korean
                if(len(twt) <=0):
                    continue

                #p = multiprocessing.Process(target=self.get_news, args=(news_info_list,twt))
                #jobs.append(p)
                self.get_news(news_info_list,twt)

            except Exception as e:
                print(e)
                
        #for p in jobs:
            #p.start()
            
        end_time  = time.time() - start_time
        logger.debug('Time on finding News: %f'% end_time )
       
        
        for j in jobs:
            j.join()

        print('result', news_info_list)

        return news_info_list

    def get_news(self,news_info_list,twt):
        
        #p_name = multiprocessing.current_process().name
        #logger.debug('%s process start', p_name)
        
        similarity_util = word2vec_similarity(self.model,self.num_feature)
        objective_words = self.read_objective_file()

        avg_vector = similarity_util.get_avg_vector(twt)
        similarity, category = \
            similarity_util.find_most_similar_category(avg_vector,objective_words)
    
        #logger.debug('%s Tweet Category:%s',p_name, category)
        logger.debug('%s Tweet Category:%s',category)
        
        #print(self.model.most_similar([avg_vector]))
        #print(similarity)
    
        #finding News
        news = self.rss_parser.parse_feed_with_word(category)
    
        #logger.info('%s Number of News Entries: %d',p_name, len(news.entries))
        logger.info('%s Number of News Entries: %d', len(news.entries))
    
    
        #can't find news
        if(len(news.entries) == 0):
            logger.warning('There is no News!!!!!!')
            return
    
        news_info = self.rss_parser.get_news_info(news)
        news_info_list.append(news_info)
        
    def get_headline_new(self):
        url ='https://news.google.com/news/rss/?hl=ko&gl=KR&ned=kr'
        news = self.rss_parser.parse_feed_with_url(url)
        
        news_info_list =[]
        news_info_list.append(self.rss_parser.get_news_info(news))
        
        return news_info_list
        
        
       

