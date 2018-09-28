# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    """
    define the spider
        :param scrapy.Spider: 
    """
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        """
        default parse method
            :param self: 
            :param response: 
        """   
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_split = ''.join(i_content.split())
                douban_item['introduce'] = content_split
            douban_item['star'] = item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = item.xpath(".//p[@class='quote']/span/text()").extract_first()
            yield douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250' + next_link, callback=self.parse)
