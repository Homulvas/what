# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3

connection = sqlite3.connect('db')
cursor = connection.cursor()
cursor.execute('''create table if not exists albums (artist text, album text, year text)''')
new = []

class WhatPipeline(object):

    def __init__(self, download_func=None):
        connection = sqlite3.connect('db')
        cursor = connection.cursor()
        cursor.execute('''create table if not exists albums (artist text, album text, year text)''')

    def process_item(self, item, spider):
        cursor.execute('''select rowid from albums where artist = ? and album = ? and year = ?''', (item['group'], item['album'], item['year']))
        data=cursor.fetchall()
        if len(data)==0:
            cursor.execute('''insert into albums values (?, ?, ?)''', (item['group'], item['album'], item['year']))
            new.append(item)
        return item

    def close_spider(self, spider):
        connection.commit()
        for item in new:
            print item
        cursor.close()