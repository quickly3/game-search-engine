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
    arg_ssid = 0
    current = 0

    def __init__(self, ssid=0, *args, **kwargs):
        super(AliSpider, self).__init__(*args, **kwargs)
        self.arg_ssid = int(ssid)

    def start_requests(self):

        ky = "doc_type:fanju && -crawl_state:*"

        if self.arg_ssid > 0:
            ky = ky + " && ssid:" + str(self.arg_ssid)


        self.count = es.count(index="fanju",q=ky);
        self.count = self.count['count']
        self.current = self.current+1



        rs = es.search(index="fanju",scroll="1m",q=ky,size=1)

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

        print("Processing: "+str(self.current)+"/"+str(self.count))

        rs = response.text
        rs =  json.loads(rs)
        print("Episode ssid:"+str(self.ssid))
        episodes = []

        episodes_doc = []

        if 'main_section' in rs['result']:
            episodes = rs['result']['main_section']['episodes'];

        if 'section' in rs['result']:
            # episodes = rs['result']['section']['episodes'];
            for section in rs['result']['section']:
                episodes.append(section);

        for episode in episodes:

            episode['doc_type'] = "episode"
            episode["ssid"] = int(self.ssid)
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

            episodes_doc.append({ "index" : { "_index" : "fanju", "_type" : "fanju" } });
            episodes_doc.append(episode)

            # es.index(index="fanju",doc_type="fanju",body=episode,routing=1)
        if len(episodes_doc) > 0:
            es.bulk(index="fanju",doc_type="fanju",body=episodes_doc,routing=1)

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
                self.current = self.current+1
                yield scrapy.Request(ss_url, self.parse)


