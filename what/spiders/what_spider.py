from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from what.items import WhatItem
import ConfigParser
import os
import string

class WhatSpider(BaseSpider):
    name = "what.cd"
    allowed_domains = ["what.cd"]
    start_urls = [
        "http://www.what.cd/login.php"
    ]


    def parse(self, response):
        config = ConfigParser.ConfigParser()
        fn = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.ini')
        config.read(fn)
        name = config.get('Login', 'Username')
        passw = config.get('Login', 'Password')
        return [FormRequest.from_response(response, formdata={'username': name, 'password': passw}, callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "Password" in response.body:
            print("Login failed???!!!")
            return
        # We've successfully authenticated, let's have some fun!
        else:
            config = ConfigParser.ConfigParser()
            fn = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.ini')
            config.read(fn)
            for dir in os.listdir(config.get('Path', 'Path')):
                yield Request('http://what.cd/artist.php?artistname=' + dir, callback=self.parse_what)
    
    def parse_what(self, response):
        x = HtmlXPathSelector(response)
        group = x.select("//div[@class='thin']/h2/text()").extract()
        albums = x.select("//tr[@class='releases_1 group discog']/td[@colspan=5]/strong/a[@title='View Torrent']/text()").extract()
        years = x.select("//tr[@class='releases_1 group discog']/td[@colspan=5]/strong/text()").extract()
        items = []
        for album, year in zip(albums, years):
            item = WhatItem()
            item['album'] = album
            item['group'] = group[0]
            item['year'] = string.split(year)[0]
            items.append(item)
        return items