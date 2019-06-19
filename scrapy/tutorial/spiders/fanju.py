# -*- coding:UTF-8 -*-
# 
#
 
import scrapy
import sys
import sqlalchemy
import os
import requests
import re
import mysql_engine
import json
from bs4 import BeautifulSoup


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



engine = mysql_engine.get_engine();


Base = declarative_base()

Session_class = sessionmaker(bind=engine)
Session = Session_class()



class AliSpider(scrapy.Spider):
    # 593
    name = "fanju"

    file = open('test.txt', 'w+')

    
    def start_requests(self):

        # 
        # https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20

        url = 'https://api.bilibili.com/pgc/web/season/section?season_id=25681'
        r=requests.get(url)#访问url
        r.encoding='utf8'

        e = json.loads(r.text)
        
        episodes = e['result']['main_section']['episodes']

        for episode in episodes:
            danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(episode['cid'])
            yield scrapy.Request(danmu_url, self.parse)


    def parse(self, response):
        lxml = BeautifulSoup(response.text,'lxml')#lxml是常用的解析器，需要提前使用pip工具安装lxml库
        danmu = lxml.find_all('d')
        # rs =  json.loads(response.text)
        for item in danmu:
            print(item.text)
            self.file.writelines(item.text+"\n\r");

