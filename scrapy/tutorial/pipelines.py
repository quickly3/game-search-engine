# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesPipeline(ImagesPipeline):
    def file_path(self,request,response=None,info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self,results,item,info):
        image_paths=[x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Failed')
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)