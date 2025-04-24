# -- coding: utf-8 --
# ***************************************************************
# Author     : John
# Data       : 2025-04-14
# Description: Scrapy 爬虫程序，用于爬取豆瓣电影 Top250 的信息。
# 创建 Scrapy 项目：在命令行中输入 scrapy startproject douban_project。
# 将上述代码保存到douban_project/spiders目录下，例如保存为douban_movie_spider.py。
# 运行爬虫：在项目根目录下，使用命令scrapy crawl douban_movie -o movies.json，这样爬取到的电影信息会保存到movies.json文件中。
# 此爬虫会提取每部电影的标题、评分和经典台词，并自动翻页抓取所有 250 条电影信息。
# ***************************************************************
import scrapy


class DoubanMovieSpider(scrapy.Spider):
    name = 'douban_movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movies = response.css('div.item')
        for movie in movies:
            yield {
                'title': movie.css('span.title::text').get(),
                'rating': movie.css('span.rating_num::text').get(),
                'quote': movie.css('span.inq::text').get()
            }

        next_page = response.css('span.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
