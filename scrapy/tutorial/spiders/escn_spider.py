# -*- coding:UTF-8 -*-
# 
#
 
import scrapy
import sys
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine("mysql+pymysql://root:root@localhost/py?charset=utf8", encoding='utf-8', echo=True)

Base = declarative_base()


Session_class = sessionmaker(bind=engine)
Session = Session_class()



class Game(Base):
    __tablename__ = 'EsDaily'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    link = Column(String(200))
    state = Column(String(200))


class AliSpider(scrapy.Spider):
    # 593
    name = "escn"
    start_urls = [
        # 'http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-604.html'
        'https://elasticsearch.cn/explore/category-18',
    ]

    def parse(self, response):
        for item in response.css('.aw-common-list .aw-item'):

            title_h4 = item.css('.aw-question-content h4')
            title = title_h4.css('a::text').extract_first();
            title = title.strip(" ");


            link = title_h4.css('a::attr(href)').extract_first();

            daily_obj = Game(title=title, link=link,state="init")    

            # if title.find("Elastic日报") > -1 :
            Session.add(daily_obj)
            Session.commit()

        next_page_li = response.css('.pagination li:nth-last-child(2)');
        next_page_a_text = next_page_li.css('a::text').extract_first();

        if next_page_a_text == ">":
            next_page_a_link = next_page_li.css('a::attr(href)').extract_first();
        else:

            next_page_li = response.css('.pagination li:nth-last-child(1)');
            next_page_a_text = next_page_li.css('a::text').extract_first();

            if next_page_a_text == ">":
                next_page_a_link = next_page_li.css('a::attr(href)').extract_first();
            else:
                next_page_a_link = none;
        

        if next_page_a_link is not None:
            yield response.follow(next_page_a_link, callback=self.parse)