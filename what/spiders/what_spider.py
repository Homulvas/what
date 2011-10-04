from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request

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
            return Request(url="http://www.what.cd", callback=self.parse_tastypage)
    
    def parse_tastypage(self, response):
        hxs = HtmlXPathSelector(response)
        yum = hxs.select('//img')
    
        # etc.