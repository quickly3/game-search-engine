# -*- coding:UTF-8 -*-
#
#

import scrapy
import sys
import sqlalchemy
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# settings.py
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..')/'.env'
load_dotenv(dotenv_path=env_path)

DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine("mysql+pymysql://"+DB_USERNAME+":"+DB_PASSWORD +
                       "@localhost/"+DB_DATABASE+"?charset=utf8", encoding='utf-8', echo=False)
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
    state = Column(Integer)


class AliSpider(scrapy.Spider):
    # 593
    name = "ali"
    start_urls = [
        # 'http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-604.html'
        'https://down.ali213.net/pcgame/all/0-0-0-0-new-pic-1',
    ]

    isDuplicate_cnt = 0
    isDuplicate = False

    def parse(self, response):

        for game in response.css('.famous-li'):
            name = game.css('.game-name::text').extract_first()
            image_url = game.css('.content-a img::attr(src)').extract_first()

            if image_url == None:
                image_url = game.css(
                    '.content-a img::attr(data-original)').extract_first()

            size = game.css('.game-down::text').extract_first()
            p1 = re.compile(r'[(](.*?)[)]', re.S)
            matches = re.findall(p1, size)
            size = matches[0]

            detail_page = "http://down.ali213.net" + \
                game.css('.content-a::attr(href)').extract_first()

            duplicate_game = Session.query(Game).filter(
                Game.detail_page == detail_page).first()

            if duplicate_game == None:
                AliSpider.isDuplicate_cnt = 0
                AliSpider.isDuplicate = False
                game_obj = Game(name=name, image_url=image_url,
                                size=size, detail_page=detail_page, state=0)
                Session.add(game_obj)
                Session.commit()
            else:
                old_game = Session.query(Game).filter(Game.detail_page == detail_page).filter(
                    sqlalchemy.text("state=1 or state=2")).first()

                if old_game != None:
                    update_obj = {
                        Game.state: 0,
                    }
                    Session.query(Game).filter(
                        Game.id == old_game.id).update(update_obj)
                    Session.commit()

                AliSpider.isDuplicate_cnt += 1
                if AliSpider.isDuplicate_cnt > 20:
                    AliSpider.isDuplicate = True
                    break

        if AliSpider.isDuplicate == True:
            next_page = None
        else:
            next_page_str = '.page-next::attr(href)'
            next_page = response.css(next_page_str).extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
