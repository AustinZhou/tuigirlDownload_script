# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
import os
from .settings import IMAGES_STORE as images_store
from scrapy.pipelines.images import ImagesPipeline

class TuigirlPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        image_link=item['download_link']
        yield scrapy.Request(image_link)

    def item_completed(self,results,item,info):
        image_path=[x["path"] for ok,x in results if ok]
        new_path=images_store+'/'+item["category_name"]+'/'+item["detail_name"]
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        os.rename(images_store+'/'+image_path[0],images_store+'/'+item["category_name"]+'/'+item["detail_name"]+'/'+item["imagefilename"])
        return item

