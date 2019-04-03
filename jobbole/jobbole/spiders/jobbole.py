# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import urlparse

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ["http://blog.jobbole.com/all-posts/"]

    def parse(self,response):
        post_urls = response.css('#archive div.floated-thumb .post-thumb a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url = post_url,callback=self.parse_detail)
        next_url = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_url:
            yield Request(url=next_url, callback=self.parse)
    def parse_detail(self,response):
        # title = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # title = response.xpath('//*[@id="post-114676"]/div[1]/h1')
        date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().encode(
            'utf8').replace("·", "").strip()
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        content = response.css("div.entry").extract()[0]
        tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()[0]
        zan = response.xpath('//div[@class="post-adds"]/span/h10/text()').extract()[0]
        sc = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        pl = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        scReStr = ".*(\d+).*"
        plReStr = ".*(\d+).*"
        pl = re.match(plReStr, pl)
        if pl:
            pl = pl.group(1)
        else:
            pl = 0
        sc = re.match(scReStr, sc)
        if sc:
            sc = sc.group(1)
        else:
            sc = 0
        print (zan)
        print (sc)
        print (date)
        print (title)
        print (content)
        print (pl)
        print (tags)
        pass