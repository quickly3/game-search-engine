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

import re

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine("mysql+pymysql://root:root@localhost/py?charset=utf8", encoding='utf-8', echo=True)

Base = declarative_base()


Session_class = sessionmaker(bind=engine)
Session = Session_class()



class EsDaily(Base):
    __tablename__ = 'EsDaily'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    link = Column(String(200))
    state = Column(String(200))


class EsDailyItem(Base):
    __tablename__ = 'EsDailyItem'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer)
    title = Column(String(200))
    link = Column(String(200))
    state = Column(String(200))


class AliSpider(scrapy.Spider):
    # 593
    name = "escn2"
    current_id = 1;
    download_link = ""
    
    def start_requests(self):
        # game_obj = Game(name=name, image_url=image_url, image_alt=image_alt, version=version, size=size, detail_page=detail_page)            
        
        try:
            esDaily = Session.query(EsDaily).filter("state='init'").order_by(EsDaily.id).first()
        except BaseException :
            print BaseException
        else:
            # self.current_data = game;
            self.current_id = esDaily.id;
            # 
            yield scrapy.Request(esDaily.link, self.parse)


    def parse(self, response):

        conuter = 0
        contents = response.css("#markdown_out::text").extract()
        links = response.css("#markdown_out a::text").extract()

        pattern = re.compile(r'^\d\.')

        for content in contents:

            content = content.replace("、",".")
            content = content.strip(" ");
            content = content.replace("\n", "");
            
            match = re.search(r'^\d\.', content)

            if match is not None:
                content = re.sub(pattern, '', content)
                link = links[conuter]

                daily_item_obj = EsDailyItem(pid=self.current_id,title=content, link=link,state="init") 
                Session.add(daily_item_obj)
                Session.commit()

                conuter+=1

        update_obj = {
            EsDaily.state:'completed',
        }

        Session.query(EsDaily).filter(EsDaily.id==self.current_id).update(update_obj)
        Session.commit();

        try:
            next_item = Session.query(EsDaily).filter("state='init'").order_by(EsDaily.id).first()
            self.current_id = next_item.id
            # next_game = Session.query(Game).filter(Game.id == self.current_id).one()
        except BaseException :
            print "All thing done."
        else:
            next_page_url = next_item.link
            yield response.follow(next_page_url, callback=self.parse)
