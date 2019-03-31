# -*- coding: utf-8 -*-
import scrapy

from douban1.items import Douban1Item

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # 循环电影的条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            # item文件导进来
            douban_item = Douban1Item()
            # 写详细的xpath,进行数据的解析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='pic']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                # 去掉空格
                content_s = "".join(i_content.split())
                douban_item["introdue"] = content_s
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # 需要将数据yield到pipelines里面去
            yield douban_item
        # 解析下一页的规则，取的后一页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse())
