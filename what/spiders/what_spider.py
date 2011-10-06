from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class WhatSpider(BaseSpider):
    name = "what.cd"
    allowed_domains = ["what.cd"]
    start_urls = [
        "http://www.what.cd/login.php"
    ]

    def parse(self, response):
        name = raw_input("name> ")
        passw = raw_input("pass> ")
        return [FormRequest.from_response(response,
                    formdata={'username': name, 'password': passw},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "login" in response.body:
            print("Login failed")
            return
        # We've successfully authenticated, let's have some fun!
        else:
            return Request(url="http://what.cd/artist.php?id=903", callback=self.parse_what)
    
    def parse_what(self, response):
        x = HtmlXPathSelector(response)
        print(x.select("//strong/a[@title='View Torrent']/text()").extract())