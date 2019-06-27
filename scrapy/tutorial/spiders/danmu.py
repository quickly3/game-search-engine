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
import logging

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch




logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("scrapy").setLevel(logging.WARNING)





engine = mysql_engine.get_engine();
Base = declarative_base()

Session_class = sessionmaker(bind=engine)
Session = Session_class()

es = Elasticsearch()
# es.indices.create(index='danmu', ignore=400)


class AliSpider(scrapy.Spider):
    # 593
    name = "danmu"
    current = 0
    
    def start_requests(self):

        self.count = es.count(index="fanju",q="doc_type:episode && -crawl_state:*");
        self.count = self.count['count']
        self.current = self.current+1


        rs = es.search(index="fanju",scroll="1m",q="doc_type:episode",size=1,sort="ssid:desc")

        self._scroll_id = rs["_scroll_id"];

        for item in rs['hits']['hits']:

            self.ssid = item['_source']["ssid"]
            # self.ss_title = item['_source']["ss_title"]
            self.cid = item['_source']["cid"]
            # self.episode = item['_source']["title"]
            self.episode_doc_id  = item['_id']

            danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(self.cid)
            yield scrapy.Request(danmu_url, self.parse)

    def parse(self, response):
        self.current = self.current+1
        print("Processing: "+str(self.current)+"/"+str(self.count))

        lxml = BeautifulSoup(response.text,'lxml')#lxml是常用的解析器，需要提前使用pip工具安装lxml库
        danmu = lxml.find_all('d')
        danmus = [];

        # print("Len: "+str(len(danmu)))
        for item in danmu:
            
            danmu = {} 
            danmu['doc_type'] = "danmu"
            danmu['danmu'] = item.text
            danmu['danmu_text'] = item.text
            danmu['danmu_p'] = item['p']


            # proptry = item['p'].split(",")
            # danmu['time_line'] = proptry[0]
            # danmu['type1'] = proptry[1]
            # danmu['type2'] = proptry[2]
            # danmu['type3'] = proptry[3]
            # danmu['send_time'] = proptry[4]
            # danmu['type4'] = proptry[5]
            # danmu['color'] = proptry[6]
            # danmu['danmu_id'] = proptry[7]

            danmu['ssid'] = self.ssid
            # danmu['ss_title'] = self.ss_title
            danmu['cid'] = self.cid
            # danmu['episode'] = self.episode

            danmu['fanju_relation'] = {
                    "name": "danmu", 
                    "parent": self.episode_doc_id 
                }

            danmus.append({ "index" : { "_index" : "fanju", "_type" : "fanju" } });
            danmus.append(danmu);
            # print(danmu)
            # es.index(index="fanju",doc_type="fanju",body=danmu,routing=1)

        es.bulk(index="fanju",body=danmus,routing=1)
        updateDate = {
            "doc":{
                "crawl_state":"finished"
            }
        }
        es.update(index="fanju",doc_type="fanju",id=self.episode_doc_id,body=updateDate)

        rs = es.scroll(scroll_id=self._scroll_id,scroll="1m")

        self._scroll_id = rs["_scroll_id"];

        if len(rs['hits']['hits']) > 0:

            for item in rs['hits']['hits']:
                self.ssid = item['_source']["ssid"]
                # self.ss_title = item['_source']["ss_title"]
                self.cid = item['_source']["cid"]
                # self.episode = item['_source']["title"]
                self.episode_doc_id  = item['_id']

                danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(self.cid)
                yield scrapy.Request(danmu_url, self.parse)

