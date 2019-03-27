# !usr/bin/env python 3.6
# -*- coding: utf-8 -*-
# Author fcj
# Time 2019-01-21
# Description 个人主页访问
import scrapy
from scrapy.http.request.form import Request
import time
import random


class FbsearchSpider(scrapy.Spider):
    name = 'fb_search'
    # allowed_domains = ['facebook.com']
    start_urls = []

    page_list = ['https://www.facebook.com/profile.php?id=100029824655082',
                 'https://www.facebook.com/aarav.aman.37',
                 'https://www.facebook.com/abilo.olibo',
                 'https://www.facebook.com/adam.doyle.520562',
                 'https://www.facebook.com/profile.php?id=100030462120558',
                 'https://www.facebook.com/advokat.marinos',
                 'https://www.facebook.com/profile.php?id=100019381960237',
                 'https://www.facebook.com/profile.php?id=100008818565707',
                 'https://www.facebook.com/blended.micx.9',
                 'https://www.facebook.com/suwat.kraweetayat.1',
                 'https://www.facebook.com/luba.boccardi',
                 'https://www.facebook.com/shannon.vitnell',
                 'https://www.facebook.com/dora.mendes.7967',
                 'https://www.facebook.com/christian.valdez.108889',
                 'https://www.facebook.com/BR33ZY123',
                 'https://www.facebook.com/dannielle.coyne',
                 'https://www.facebook.com/ben.degan.714',
                 'https://www.facebook.com/mariusz.jaroszek.3',
                 'https://www.facebook.com/qihui.lan',
                 'https://www.facebook.com/emil.wilk.7']

    def start_requests(self):
        for index in range(1, 2000):
            result_url, ph = self.random_url()
            yield Request(
                url=''.join(random.sample(self.page_list, 1)),
                headers={
                    'authority': 'www.facebook.com',
                    'method': 'GET',
                    'path': ph,
                    'scheme': 'https',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'dnt': '1',
                    'upgrade-insecure-requests': '1',
                },
                cookies={
                    'sb': '',
                    'datr': '',
                    'm_pixel_ratio': '1',
                    'pl': 'n',
                    'xs': '',
                    'c_user': '',
                    # 'spin': '',
                    'fr': '',
                    'wd': ''
                },
                callback=self.parse,
                errback=self.error,
                dont_filter=True,  # 让结果重复出现
                meta={'proxy': 'http://:1080'}
            )

    def random_url(self):
        url_list = self.page_list
        result_url = ''.join(random.sample(url_list, 1))
        ph = '/' + str(result_url).split('/')[-1]
        return result_url, ph

    def parse(self, response):
        result = response.body.decode('utf-8')

        if '暂时禁止' not in result:
            print('cookie is fine, so we go on')
        else:
            print('cookie maybe time out and please check account')

        with open('facebook.html', 'w', encoding='utf-8') as ff:
            ff.write(result)
            ff.close()

        time.sleep(random.randint(15, 30))

    def error(self, response):

        pass


