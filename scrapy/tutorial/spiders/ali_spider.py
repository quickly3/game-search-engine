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
    __tablename__ = 'Game'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    image_url = Column(String(200))
    image_alt = Column(String(200))
    version = Column(String(200))
    size = Column(String(50))
    detail_page = Column(String(200))


class AliSpider(scrapy.Spider):
    # 593
    name = "ali"
    start_urls = [
        # 'http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-604.html'
        'http://down.ali213.net/pcgame/',
    ]

    def parse(self, response):
        for game in response.css('.list_body_con'):
            name = game.css('.list_body_con_con a::text').extract_first();
            image_url = game.css('.list_body_con_img img::attr(data-original)').extract_first();
            image_alt = game.css('.list_body_con_img img::attr(alt)').extract_first();
            version = game.css('.list_body_con_img_bg span::text').extract_first();
            size = game.css('.list_body_con_pf .text::text').extract_first();
            detail_page = "http://down.ali213.net"+game.css('.list_body_con_down::attr(href)').extract_first();


            print name
            # data_obj = {
            #     'name':name ,
            #     'image_url':image_url ,
            #     'image_alt':image_alt ,
            #     'version':version ,
            #     'size':size ,
            #     'detail_page':detail_page ,
            # }

            game_obj = Game(name=name, image_url=image_url, image_alt=image_alt, version=version, size=size, detail_page=detail_page)            
            Session.add(game_obj)
            Session.commit()

            # print data_obj;

        next_page_str = '.list_body_page a[title=下一页]::attr(href)';

        next_page = response.css(next_page_str).extract_first()

        if next_page is not None:

            yield response.follow(next_page, callback=self.parse)