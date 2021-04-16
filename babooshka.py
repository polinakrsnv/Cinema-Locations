from scrapy.spiders import Rule, CrawlSpider
import scrapy
from scrapy import Spider
from scrapy import Field, Item
from scrapy import Request
import json
FEED_EXPORT_ENCODING = 'utf-8'

class field(Item):
    Title = Field()
    Link = Field()
    Description = Field()
    Photo = Field()
    new_link = Field()

class BabooshkaSpider(scrapy.Spider):

    name = "babooshka"
    start_urls = ["https://babooshka.pro"]

    def parse(self, response):
        item = field()

        for links in response.xpath('//li[@class=""]'):
            next_link = "https://babooshka.pro" + str(links.xpath('a/@data-path').extract())[2:-2]
            #print(next_link)
            sub = links.xpath('div[@class="subKat"]/ul/li')
            for s in sub:
                next_link_ = next_link + str(s.xpath('a/@data-build').extract())[2:-2]
                #print(next_link_)
                yield Request(next_link_, callback=self.parse_tag)

    def parse_tag(self, response):
        for links in response.xpath('//h3/a'):
            next_object = response.url + "/" + str(links.xpath('@title').extract())[2:-2] + "/"
            #print(next_object)
            yield Request(next_object, callback=self.parse_object)

    def parse_object(self, response):
        item = field()
        title = response.xpath('//h3/text()')[0].extract()
        if title == "# ":
            return
        item['Title'] = title
        item['Link'] = response.url
        description = response.xpath('//p/text()').extract()
        #if description[0] == " ":
            #del description[0]
        del description[-1]
        del description[-1]
        del description[-1]
        if description and description[-1] == " \t\t\t\t\t\t\t\t":
            del description[-1]
        item['Description'] = description
        images_list = []
        for image in response.xpath('//div[@class="row imagespop"]/div/a/img/@src').extract():
            images_list.append("https://babooshka.pro" + str(image))
        item['Photo'] = images_list
        return item

