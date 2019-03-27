# !usr/env/bin python 3.6
# -*- coding: utf-8 -*-
# author fcj
# time 2018-12-28
# 整个scarpy项目的setting文件

# Scrapy settings for FacebookCrawler project

# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FacebookCrawler'

SPIDER_MODULES = ['FacebookCrawler.spiders']
NEWSPIDER_MODULE = 'FacebookCrawler.spiders'

SPLASH_URL = 'http://127.0.0.1:8050/'  # splash 默认接口url

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SPIDER_MIDDLEWARES = {
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# scrapy-splash的中间插件设置
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# 默认 USER-AGENT 在splash请求中可以设置
DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/71.0.3578.98 Safari/537.36 Avast/71.0.1037.99',}
# 管道 管道稍后在设置
# ITEM_PIPELINES = {'news.pipelines.NewsPipeline': 300,}

# scrapy-spalsh存储等接口中间插件
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

DOWNLOAD_DELAY = 5  # 发包延时
CONCURRENT_REQUESTS = 16  # 最大并发数


FEED_EXPORT_ENCODING = 'utf-8'  # 改结果输出为 utf-8
