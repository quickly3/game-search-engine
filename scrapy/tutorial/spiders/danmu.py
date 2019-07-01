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
import datetime
import zipfile

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch

logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("scrapy").setLevel(logging.WARNING)

storage_dir = '../storage/fanju'

if not os.path.isdir(storage_dir):
    os.mkdir( storage_dir );

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
    arg_ssid = 0
    
    def __init__(self, ssid=0, *args, **kwargs):
        super(AliSpider, self).__init__(*args, **kwargs)
        self.arg_ssid = int(ssid)

    def start_requests(self):
        ky = "doc_type:episode && cid:* && -crawl_state:*"

        if self.arg_ssid > 0:
            ky = ky + " && ssid:" + str(self.arg_ssid)

        self.count = es.count(index="fanju",q=ky);
        self.count = self.count['count']
        self.current = self.current+1

        rs = es.search(index="fanju",scroll="1m",q=ky,size=1)

        self._scroll_id = rs["_scroll_id"];

        for item in rs['hits']['hits']:

            self.ssid = int(item['_source']["ssid"])
            self.fanju_title = item['_source']["fanju_title"]

            if "episode_title" in item['_source']:
                self.episode_title = item['_source']["episode_title"]
            else:
                self.episode_title = ""

            self.episode_no = item['_source']["episode_no"]

            self.cid = item['_source']["cid"]
            
            # self.episode = item['_source']["title"]
            self.episode_doc_id  = item['_id']
            

            self.danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(self.cid)
            yield scrapy.Request(self.danmu_url, self.parse)

    def parse(self, response):

        print("Processing: "+str(self.current)+"/"+str(self.count))

        lxml = BeautifulSoup(response.text,'lxml')#lxml是常用的解析器，需要提前使用pip工具安装lxml库
        danmu = lxml.find_all('d')
        danmus = [];

        self.fanju_title = self.fanju_title.replace("/","|")
        self.fanju_title = self.fanju_title.replace("|"," ")
        self.fanju_title = self.fanju_title.replace('"'," ")

        episode_path = storage_dir+"/"+self.fanju_title

        episode_zip_filename  = storage_dir+"/"+self.fanju_title+".zip"

        if not os.path.isdir(storage_dir):
            os.mkdir( storage_dir );

        if not os.path.isdir(episode_path):
            os.mkdir( episode_path );

        self.episode_title = self.episode_title.replace("/"," ")
        self.episode_title = self.episode_title.replace('"'," ")
        self.episode_title = self.episode_title.replace("|"," ")
        self.episode_title = self.episode_title.replace("?","？")


        if self.episode_title == "":
            file_path =  episode_path+str(self.episode_no)+".txt"
        else:
            file_path =  episode_path+"/第" + str(self.episode_no) + "话 - " +self.episode_title+".txt"


        file = open(file_path, 'w+',encoding="utf-8")

        # print("Len: "+str(len(danmu)))
        for item in danmu:
            
            file.write(item.text+"\n")    

            danmu = {} 
            danmu['doc_type'] = "danmu"
            danmu['danmu'] = item.text
            danmu['danmu_text'] = item.text
            # danmu['danmu_p'] = item['p']


            proptry = item['p'].split(",")
            danmu['time_line'] = proptry[0]
            #type
            danmu['danmu_type'] = proptry[1]
            #size
            danmu['size'] = proptry[2]
            #color_id
            danmu['decimal_color'] = proptry[3]
            danmu['send_time'] = int(proptry[4])
            danmu['send_time'] = datetime.datetime.fromtimestamp(danmu['send_time']);

            # is_captions
            danmu['is_captions'] = proptry[5]
            #uhash
            danmu['uhash'] = proptry[6]
            danmu['danmu_id'] = proptry[7]

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

        # es.bulk(index="fanju",body=danmus,routing=1)

        # episode_path = episode_path.replace(" ","_")
        # episode_zip_filename = episode_zip_filename.replace(" ","_")
        # print(episode_path)
        # print(episode_zip_filename)

        self.zipDir(episode_path,episode_zip_filename)

        updateDate = {
            "doc":{
                "crawl_state":"finished"
            }
        }
        es.update(index="fanju",doc_type="fanju",id=self.episode_doc_id,body=updateDate)

        fanju = es.search(index="fanju",doc_type="fanju",q="doc_type:fanju && ssid:"+str(self.ssid) )

        if fanju['hits']['total'] > 0:
            fanju_doc_id = fanju['hits']['hits'][0]["_id"]
            updateDate = {
                "doc":{
                    "danmu_dir":episode_path,
                    "danmu_zip":episode_zip_filename,
                }
            }            
            es.update(index="fanju",doc_type="fanju",id=fanju_doc_id,body=updateDate)

        rs = es.scroll(scroll_id=self._scroll_id,scroll="1m")

        self._scroll_id = rs["_scroll_id"];

        if len(rs['hits']['hits']) > 0:

            for item in rs['hits']['hits']:
                self.ssid = item['_source']["ssid"]
                self.fanju_title = item['_source']["fanju_title"]

                if "episode_title" in item['_source']:
                    self.episode_title = item['_source']["episode_title"]
                else:
                    self.episode_title = ""

                self.episode_no = item['_source']["episode_no"]
                
                self.cid = item['_source']["cid"]
                # self.episode = item['_source']["title"]
                self.episode_doc_id  = item['_id']
                self.current = self.current+1
                self.danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(self.cid)
                yield scrapy.Request(self.danmu_url, self.parse)

    def zipDir(self,dirpath,outFullName):

        zip = zipfile.ZipFile(outFullName,"w")

        for path,dirnames,filenames in os.walk(dirpath):
            
            fpath = path.replace(dirpath,'')

            for filename in filenames:
                zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
        zip.close()