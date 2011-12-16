from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from what.items import WhatItem
import ConfigParser
import os

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
        name = config.get('SectionOne', 'Username')
        passw = config.get('SectionOne', 'Password')
        return [FormRequest.from_response(response,
                    formdata={'username': name, 'password': passw},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "Password" in response.body:
            print("Login failed???!!!")
            return
        # We've successfully authenticated, let's have some fun!
        else:
            return Request(url="http://what.cd/artist.php?id=903", callback=self.parse_what)
    
    def parse_what(self, response):
        x = HtmlXPathSelector(response)
        albums = x.select("//tr[@class='releases_1 group discog']/td[@colspan=5]/strong/a[@title='View Torrent']/text()").extract()
        items = []
        for album in albums:
            item = WhatItem()
            item['name'] = album
            items.append(item)
        return items