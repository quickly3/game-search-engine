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



class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    # name = Column(String(200))
    # image_url = Column(String(200))
    # image_alt = Column(String(200))
    # version = Column(String(200))
    # size = Column(String(50))
    # detail_page = Column(String(200))

    # appid = Column(Integer)
    # conid = Column(Integer)
    # download_page = Column(String(200))
    # name_chs = Column(String(200))
    # inLanguage = Column(String(200))
    # license = Column(String(200))
    # name_en = Column(String(200))
    # game_type = Column(String(200))
    # publisher = Column(String(200))
    # publish_date_by_ali = Column(String(200))
    # game_tags_string = Column(Text)
    # game_images_mini_string = Column(Text)
    # game_images_string = Column(Text)
    # description = Column(Text)
    # sys_requirements = Column(Text)
    # install_info = Column(Text)
    # soft_requirements = Column(Text)


    # state = Column(Integer)

class AliSpider(scrapy.Spider):
    # 593
    name = "nba_player"
    start_urls = [
        # 'http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-604.html'
        'http://www.stat-nba.com/query.php?QueryType=all&AllType=season&AT=avg&order=1&crtcol=pts&PageNum=20',
    ]

    def parse(self, response):
        stat_box = response.css('table.stat_box')

        for tr in stat_box.css('tr'):
            tds = tr.css('td');
            name_cn = tds.css(':nth-child(2)::text').extract_first()
            _id = tds.css(':nth-child(1)::text').extract_first()
            link = tds.css(':nth-child(2)::attr(href)').extract_first()
            games_played = tds.css(':nth-child(3)::text').extract_first()
            start = tds.css(':nth-child(4)::text').extract_first()
            minutes = tds.css(':nth-child(5)::text').extract_first()

            field_goal_percentage = tds.css(':nth-child(6)::text').extract_first()
            field_goal_score = tds.css(':nth-child(7)::text').extract_first()
            field_goal_shot = tds.css(':nth-child(8)::text').extract_first()

            three_point_percentage = tds.css(':nth-child(9)::text').extract_first()
            three_point_score = tds.css(':nth-child(10)::text').extract_first()
            three_point_shot = tds.css(':nth-child(11)::text').extract_first()

            free_throw_percentage = tds.css(':nth-child(12)::text').extract_first()
            free_throw_score = tds.css(':nth-child(13)::text').extract_first()
            free_throw_shot = tds.css(':nth-child(14)::text').extract_first()

            backboard = tds.css(':nth-child(15)::text').extract_first()
            front_court = tds.css(':nth-child(16)::text').extract_first()
            back_court = tds.css(':nth-child(17)::text').extract_first()
            assist = tds.css(':nth-child(18)::text').extract_first()
            steal = tds.css(':nth-child(19)::text').extract_first()
            block_shot = tds.css(':nth-child(20)::text').extract_first()

            turnover = tds.css(':nth-child(21)::text').extract_first()
            foul = tds.css(':nth-child(22)::text').extract_first()
            scoring = tds.css(':nth-child(23)::text').extract_first()

            win = tds.css(':nth-child(24)::text').extract_first()
            lose  = tds.css(':nth-child(25)::text').extract_first()

            print lose





