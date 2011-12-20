# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3

class WhatPipeline(object):

    def __init__(self):
        self.connection = sqlite3.connect('db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''create table if not exists albums (artist text, album text, year text)''')
        self.new = []

    def process_item(self, item, spider):
        self.cursor.execute('''select rowid from albums where artist = ? and album = ? and year = ?''', (item['group'], item['album'], item['year']))
        data = self.cursor.fetchall()
        if len(data)==0:
            self.cursor.execute('''insert into albums values (?, ?, ?)''', (item['group'], item['album'], item['year']))
            new.append(item)
        return item

    def close_spider(self, spider):
        self.connection.commit()
        for item in self.new:
            print item
        self.cursor.close()