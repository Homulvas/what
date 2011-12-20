# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3

connection = sqlite3.connect('db')
cursor = connection.cursor()
cursor.execute('''create table if not exists albums (artist text, album text, year text)''')

class WhatPipeline(object):
    def process_item(self, item, spider):
        return item
