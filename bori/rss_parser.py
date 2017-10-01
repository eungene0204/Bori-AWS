import feedparser
import urllib.request
from bs4 import BeautifulSoup

class rss_parser():
    
    def __init__(self):
        self.header = 'http://news.google.co.kr/news?hl=ko&ned=kr&ie=UTF-8&q='
        self.tail = '&output=rss'
    
    def encode_objective_word(self,word):
        endcoded_word = urllib.parse.quote(word.encode('utf8'))
        
        return endcoded_word
        
    def parse_feed(self,word):
        #d = feedparser.parse('http://news.google.co.kr/news?hl=ko&ned=kr&ie=UTF-8&q=%EC%86%8C%EC%84%A4&output=rss')
        word = self.encode_objective_word(word)
        url = self.header + word + self.tail
        news = feedparser.parse(url)
        return news
    
    def get_img_src(self,summary):
        soup = BeautifulSoup(summary)
        img_src = soup.find('img').get('src')
        
        return img_src
    
    def get_news_info(self,news):
        post_list = []
        
        #print('news')
        #print(news)
        print(len(news.entries))
        
        for post in news.entries:
           
            #print('post')
            #print(post)

            summary = post['summary']
            #print('summary')
            #print(summary)
            img_src = self.get_img_src(summary)
            
            #print('img src')
            #print(img_src)
            
            title = post['title']
            link = post['link']
            
            id = post['id']
            print('id')
            print(id)
            
            print('link')
            print(link)
            
            news_dict = {'id':id, 'title':title, 'link':link, 'img_src': img_src}
            post_list.append(news_dict)
        
        return post_list
   












