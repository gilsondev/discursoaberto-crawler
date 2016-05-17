# -*- coding: utf-8 -*-

import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DiscursoPipeline(object):
    def process_item(self, item, spider):
        item['inserted_at'] = datetime.datetime.utcnow()
        item['created_at'] = datetime.datetime.strptime(
            item['created_at'], "%d/%m/%Y %H:%M")
        return item
