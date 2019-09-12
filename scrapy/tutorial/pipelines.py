# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os
import requests
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class TutorialPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        return item


class ImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        # print("Hello")
        # print(image_paths)

        if not image_paths:
            raise DropItem('Image Download Failed')
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)


# -*- coding: utf-8 -*-


class HupuGifPipeline(ImagesPipeline):
    def process_item(self, item, spider):

        if 'image_urls' in item:
            images = []

        dir_path = '%s/%s' % (settings.get('IMAGES_STORE'), spider.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for image_url in item['image_urls']:
            us = image_url.split('/')[-1]
            file_path = '%s/%s' % (dir_path, us)
            images.append(file_path)
            if os.path.exists(file_path):
                continue
            with open(file_path, 'wb') as handle:
                response = requests.get(image_url, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

        item['images'] = images
        return item
