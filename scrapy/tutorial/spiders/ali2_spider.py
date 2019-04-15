# -*- coding:UTF-8 -*-
# 
#
 
import scrapy
import sys
import sqlalchemy
import os
import urlparse 
import json
import re

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine("mysql+pymysql://root:root@localhost/py?charset=utf8", encoding='utf-8', echo=True)

Base = declarative_base()


Session_class = sessionmaker(bind=engine)
Session = Session_class()

dr = re.compile(r'<[^>]+>',re.S)



class Game(Base):
    __tablename__ = 'Game'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    image_url = Column(String(200))
    image_alt = Column(String(200))
    version = Column(String(200))
    size = Column(String(50))
    detail_page = Column(String(200))

    appid = Column(Integer)
    conid = Column(Integer)
    download_page = Column(String(200))
    name_chs = Column(String(200))
    inLanguage = Column(String(200))
    license = Column(String(200))
    name_en = Column(String(200))
    game_type = Column(String(200))
    publisher = Column(String(200))
    publish_date_by_ali = Column(String(200))
    game_tags_string = Column(Text)
    game_images_mini_string = Column(Text)
    game_images_string = Column(Text)
    description = Column(Text)
    sys_requirements = Column(Text)
    install_info = Column(Text)
    soft_requirements = Column(Text)

    

    state = Column(Integer)


class Ali2Spider(scrapy.Spider):
    # 593
    name = "ali2"
    current_id = 1;
    download_link = "http://www.soft5566.com/down/{ali_id}-1.html"
    # start_urls = [
    #     'http://down.ali213.net/pcgame/all/0-0-0-0-new-pic-604.html'
    #     # 'http://down.ali213.net/pcgame/',
    # ]

    def start_requests(self):
        # game_obj = Game(name=name, image_url=image_url, image_alt=image_alt, version=version, size=size, detail_page=detail_page)            
        
        try:
            game = Session.query(Game).filter("state=0").order_by(Game.id).first()
        except BaseException :
            print BaseException
        else:
            # self.current_data = game;
            self.current_id = game.id;
            # 
            yield scrapy.Request(game.detail_page, self.parse)




        
    def parse(self, response):

        id_zone_url = response.css('#ali_comment_pc_global::attr(src)').extract_first();

        if id_zone_url != None:
            query = urlparse.urlparse(id_zone_url).query
            params = dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])

            game_ids = params['sid'].split("-")

            appid = game_ids[0];
            conid = game_ids[1];
        else:
            id_zone_url = response.css('#ali_hits_pc_global::attr(src)').extract_first();

            query = urlparse.urlparse(id_zone_url).query
            params = dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])

            appid = params['entityID']
            conid = params['channelID']



        download_page = self.download_link.replace("{ali_id}",conid);

        name_chs = response.css('.detail_game_l_r_ctit h1::text').extract_first();
        name_chs = dr.sub('',name_chs)

        inLanguage = response.css('.detail_game_l_r_ctit span[itemprop=inLanguage]::text').extract_first();
        license = response.css('.detail_game_l_r_ctit span[itemprop=license]::text').extract_first();
        name_en = response.css('.detail_game_l_r_ctit span[itemprop=alias]::text').extract_first();
        
        game_type = response.css('.detail_game_l_r_info ul li')[0].css("a::text").extract_first();

        publish_date_by_ali = response.css('.detail_game_l_r_info ul li')[1].css("a span::text").extract_first();

        publisher = response.css('.detail_game_l_r_info ul li')[2].css("::text").extract_first();
        publisher = publisher.split("：")[1]

        game_tags = response.css('.detail_game_l_r_tag a::text').extract();

        game_tags_string = ",".join(game_tags)

        game_images_mini_string = "";
        game_images_mini = response.css('#smallImg span img::attr(src)').extract();
        if len(game_images_mini) > 0 :
            game_images_mini.pop();
            game_images_mini_string = ",".join(game_images_mini)

        game_images_string = "";
        game_images = response.css('.detail_body_con_bb_con_con .detail_body_con_jt_con_img img::attr(src)').extract();
        if len(game_images) > 0 :
            game_images.pop();
            game_images_string = ",".join(game_images)


        description = ""
        #  detail_body_con_bb_con1
        description_arr = response.css('#yxjs .detail_body_left_info_con p').extract();
        

        if len(description_arr) > 0 :
            description = "".join(description_arr)

        # if description != None:
        #     description = dr.sub('',description)

        # print description;
        # os._exit()

        sys_requirements = ""
        install_info = ""
        soft_requirements = ""

        gameSetting = response.css('#pzyq .detail_body_left_info_con .gameSetting ul');

        if len(gameSetting) > 0:

            sys_requirements_key = gameSetting[0].css('li span::text').extract();
            sys_requirements_value1 = gameSetting[1].css('li span::text').extract();
            sys_requirements_value2 = gameSetting[2].css('li span::text').extract();

            sys_requirements = [];

            for i in xrange(0,len(sys_requirements_key)):
                item = {}
                item['key'] = sys_requirements_key[i]
                item['v1']  = sys_requirements_value1[i]
                item['v2']  = sys_requirements_value2[i]
                sys_requirements.append(item);

            sys_requirements = json.dumps(sys_requirements)

        install_info = response.css('#azsm .detail_body_left_info_con p::text').extract();
        install_info = ",".join(install_info)

        soft_requirements = response.css('.yunxingku ul li').extract();

        soft_requirements = ",".join(soft_requirements)

        soft_requirements = soft_requirements.replace('<li>',"");
        soft_requirements = soft_requirements.replace('</li>',"");


        update_obj = {
            Game.state:1,
            Game.appid:appid,
            Game.conid:conid,
            Game.download_page:download_page,
            Game.name_chs:name_chs,
            Game.name_en:name_en,
            Game.inLanguage:inLanguage,
            Game.license:license,
            Game.game_type:game_type,
            Game.publisher:publisher,
            Game.publish_date_by_ali:publish_date_by_ali,
            Game.game_tags_string:game_tags_string,
            Game.game_images_mini_string:game_images_mini_string,
            Game.game_images_string:game_images_string,
            Game.description:description,
            Game.sys_requirements:sys_requirements,
            Game.install_info:install_info,
            Game.soft_requirements:soft_requirements
        }

        Session.query(Game).filter(Game.id==self.current_id).update(update_obj)
        Session.commit();


        # self.current_id += 1;

        try:
            next_game = Session.query(Game).filter("state=0").order_by(Game.id).first()
            self.current_id = next_game.id
            # next_game = Session.query(Game).filter(Game.id == self.current_id).one()
        except BaseException :
            print "All thing done."
        else:
            next_page_url = next_game.detail_page + '?_=' + str(next_game.id);
            yield response.follow(next_page_url, callback=self.parse)


            