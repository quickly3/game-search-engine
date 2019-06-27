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

from urllib.parse import urlparse,parse_qs
from elasticsearch import Elasticsearch

es = Elasticsearch()

engine = mysql_engine.get_engine();


Base = declarative_base()

Session_class = sessionmaker(bind=engine)
Session = Session_class()


class AliSpider(scrapy.Spider):
    # 593
    name = "episode"
    ssid = 0
    
    def start_requests(self):

        rs = es.search(index="fanju",scroll="1m",q="doc_type:fanju && -crawl_state:*",size=1)

        self._scroll_id = rs["_scroll_id"];

        for item in rs['hits']['hits']:
            link = item['_source']['link']

            self.ssid = link.replace("https://www.bilibili.com/bangumi/play/ss","")
            self.fanju_title = item['_source']['fanju_title']
            self.fanju_doc_id  =  item['_id']

            ss_url = 'https://api.bilibili.com/pgc/web/season/section?season_id={_ss_id}'
            ss_url = ss_url.format(_ss_id=self.ssid)

            yield scrapy.Request(ss_url, self.parse)

    def parse(self, response):
        rs = response.text
        rs =  json.loads(rs)

        episodes = []

        if 'main_section' in rs['result']:
            episodes = rs['result']['main_section']['episodes'];

        if 'section' in rs['result']:
            # episodes = rs['result']['section']['episodes'];
            for section in rs['result']['section']:
                episodes.append(section);


        for episode in episodes:

            episode['doc_type'] = "episode"
            episode["ssid"] = self.ssid
            episode["fanju_title"] = self.fanju_title

            if 'long_title' in episode:
                episode['episode_title'] = episode['long_title']
                episode['episode_title_text'] = episode['long_title']
                del episode['long_title']

            
            if 'title' in episode:
                episode['episode_no'] = episode['title']
                del episode['title']

            episode['fanju_relation'] = {
                    "name": "episode", 
                    "parent": self.fanju_doc_id 
                }
            es.index(index="fanju",doc_type="fanju",body=episode,routing=1)

        updateDate = {
            "doc":{
                "crawl_state":"finished"
            }
        }
        es.update(index="fanju",doc_type="fanju",id=self.fanju_doc_id,body=updateDate)

        body = { "scroll" : "1m", "scroll_id" : self._scroll_id };

        rs = es.scroll(scroll_id=self._scroll_id,scroll="1m")

        self._scroll_id = rs["_scroll_id"];

        if len(rs['hits']['hits']) > 0:

            for item in rs['hits']['hits']:
                link = item['_source']['link']
                self.ssid = link.replace("https://www.bilibili.com/bangumi/play/ss","")
                self.fanju_title = item['_source']['fanju_title']
                self.fanju_doc_id  =  item['_id']

                ss_url = 'https://api.bilibili.com/pgc/web/season/section?season_id={_ss_id}'
                ss_url = ss_url.format(_ss_id=self.ssid)

                yield scrapy.Request(ss_url, self.parse)


