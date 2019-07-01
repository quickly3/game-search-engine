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
import datetime

from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from elasticsearch import Elasticsearch


engine = mysql_engine.get_engine();
storage_dir = '../storage/fanju'

if not os.path.isdir(storage_dir):
    os.mkdir( storage_dir );

Base = declarative_base()

Session_class = sessionmaker(bind=engine)
Session = Session_class()


es = Elasticsearch()
es.indices.create(index='fanju', ignore=400)


class AliSpider(scrapy.Spider):
    # 593
    name = "fanju"

    # 
    page = 1

    start_urls = [
        'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20',
    ]

    def parse(self, response):
        rs =  json.loads(response.text)

        items = rs['result']['data']

        fanjus = []

        for item in items:
            item['doc_type'] = "fanju"
            follow_dealed = False
            play_dealed = False

            if 'score' in item['order']:
                score = item['order']['score'] 
                item['order']['score']  = score.replace("分","");


            if int(item['order']['pub_date']) > 0:
                 item['order']['pub_date']  = datetime.datetime.fromtimestamp(item['order']['pub_date']);
            else:
                del item['order']['pub_date']

            if int(item['order']['pub_real_time']) > 0:
                item['order']['pub_real_time']  = datetime.datetime.fromtimestamp(item['order']['pub_real_time']);
            else:
                del item['order']['pub_real_time']

            
            if 'renewal_time' in item['order']:
                item['order']['renewal_time']  = datetime.datetime.fromtimestamp(item['order']['renewal_time']);

            item['order']['follow_string'] = item['order']['follow']
            item['order']['play_string'] = item['order']['play']

            item['order']['follow'] = item['order']['follow'].replace("人追番","")
            item['order']['follow'] = item['order']['follow'].replace("人想看","")


            if "万" in item['order']['follow']:
                item['order']['follow'] = item['order']['follow'].replace("万","")
                item['order']['follow'] = float(item['order']['follow']) * 10000
                follow_dealed = True

            if not follow_dealed and ("亿" in item['order']['follow']) :
                item['order']['follow'] = item['order']['follow'].replace("亿","")
                item['order']['follow'] = float(item['order']['follow']) * 100000000
                follow_dealed = True
                
            item['order']['play'] = item['order']['play'].replace("次播放","");

            if "万" in item['order']['play']:
                item['order']['play'] = item['order']['play'].replace("万","")
                item['order']['play'] = float(item['order']['play']) * 10000
                play_dealed = True

            if not play_dealed and "亿" in item['order']['play']:
                item['order']['play'] = item['order']['play'].replace("亿","")
                item['order']['play'] = float(item['order']['play']) * 100000000
                play_dealed = True

            if not play_dealed and "--" in item['order']['play']:
                item['order']['play'] = 0
                play_dealed = True

            for key in item['order']:
                item[key] = item['order'][key]
            
            item['fanju_title'] = item['title']
            item['fanju_title_text'] = item['title']

            del item['order']
            del item['title']

            if 'index_show' in item:
                
                # item['episode'] = item['index_show'].replace("更新至","").replace("更新至第","").replace("全","").replace("第","").replace("话","").replace("已完结","").replace("即将开播","");
                pattern = re.compile(r'[\u4e00-\u9fa5]')
                item['episode'] = re.sub(pattern, '', item['index_show'])
                item['episode'] = item['episode'].replace("-",".")
                item['episode'] = item['episode'].strip()
                if item['episode'] == "":
                    item['episode'] = 0
                else:
                    item['episode'] = float(item['episode'])

            item['ssid'] = int(item['link'].replace("https://www.bilibili.com/bangumi/play/ss",""))

            item['fanju_relation'] = "fanju"

            fanjus.append({ "index" : { "_index" : "fanju", "_type" : "fanju" } });
            fanjus.append(item)

            # try:
            #     es.index(index="fanju",doc_type="fanju",body=item)
            # except BaseException :
            #     print("Error")
            #     print(item)
            #     sys.exit()

        es.bulk(index="fanju",body=fanjus,routing=1)

        next_page_url = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={_page}&season_type=1&pagesize=20'
        
        self.page = self.page+1
        next_page_url = next_page_url.format(_page=self.page);
        next_page=requests.get(next_page_url)#访问url
        next_page.encoding='utf8'
        next_page_text = json.loads(next_page.text)
        next_page_item_cnt = len(next_page_text['result']['data'])

        if next_page_item_cnt > 0:
            yield response.follow(next_page_url, callback=self.parse)
