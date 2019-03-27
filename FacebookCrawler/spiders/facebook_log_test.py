# !usr/bin/env python 3.6
# -*- coding: utf-8 -*-
# Author fcj
# Time 2019-01-14
# Description facebook登录测试

import scrapy
from scrapy_splash import SplashFormRequest
from scrapy.http.request.form import Request
import json
from FacebookCrawler.extract_html import del_serach_result
from facebook import GraphAPI
import execjs


coo = 'datr=; fr=' \
      'AWUF_Zi6; sb=_; c_user=; xs=' \
      '3A-1; pl=n; m_pixel_ratio=1; wd=1920x976'
# facebook lua设置登录脚本,cookie登录用这个，需要cookie、user_agent
zero = '''
function main(splash, args)
    splash:set_viewport_full()
    splash:go(args.url)
    splash:wait(math.random(3,5))
'''
#  top_html 搜索结果主页面、 user_html 用户页面、 public_html 公共主页页面  三个html文本
# splash:wait(math.random(5,8))
# top_html = splash:html()   top_html 暂不提取，以后有需求可添加进来，放在user_href前即可

zero_end = '''
    splash:wait(math.random(1,3))
    search_key = args.search_key
    search_text = splash:select('.inputtext')
    search_btn = splash:select('button[type=submit]')
    
    if (search_text and search_btn) then
        search_text: send_text(search_key)
        search_btn: mouse_click({})    
    end
    splash:wait(math.random(1,3))
    
    user_href = splash:select('li[data-edge=keywords_users]')
    if user_href then
        user_href: mouse_hover({x=0, y=0})
        user_href: mouse_click({})
        
    end
    splash:wait(math.random(1,3))
    user_html = splash:html()
        
    public_href = splash:select('li[data-edge=keywords_pages]')
    if public_href then
        public_href: mouse_hover({x=0, y=0})
        public_href: mouse_click({})
    end
    splash:wait(math.random(1,3))
    public_html = splash:html()
      
    return {
    
    cookies=splash:get_cookies()
    }
end
'''
get_cookie = 'splash:runjs("function setCookie('+coo+') { var list = t.split("; ");' \
             'for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; ' \
             'var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); ' \
             'var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); ' \
             'document.cookie += cname + "+" + cvalue + "; " + expires+"~"; } return document.cookie } ")'
cookie_end = '''
    return {splash:har(),splash:get_cookies()}
end
'''

mobile_end = '''
    splash:wait(math.random(3,6))
    
    search_key = args.search_key
    search_text = splash:select('[type=search]')
    search_btn = splash:select('#u_0_f')
    

    if (search_text and search_btn) then
        search_btn: mouse_click({})
        search_text: send_text(search_key)
        splash:send_keys("key_Enter")
    end
    
    splash:wait(math.random(3,6))
    
    splash:wait(math.random(3,5))  
    return {
    
    cookies=splash:get_cookies()
    }
end
'''
five = '    splash:runjs("javascript:void(function(){ function setCookie(t) { var list = t.split(\'; \');' \
       ' console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split(\'=\')[0];' \
       ' var c_value = list[i].split(\'=\')[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000));' \
       ' var expires = \';domain=.facebook.com;expires=\'+ d.toUTCString(); document.cookie = cname + \'=\' +' \
       ' c_value + \'; \' + expires; } }  var cookie = \''+coo+'\'; setCookie(cookie); location.href =' \
       ' \'https://www.facebook.com\'; })();")'  # https://mobile.facebook.com H5页面 https://www.facebook.com 电脑web

lg = zero+'\n'+five+'\n'+zero_end


class FacebookLogTestSpider(scrapy.Spider):
    name = 'facebook_log_test'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    login_url = 'https://www.facebook.com/login'
    start_urls = []
    search_key = 'Michael '

    def start_requests(self):  # 起点主要作用是回调splash

        yield Request(
            url=self.login_url,
            callback=self.login,
            meta={'proxy': 'http://:1080'}
        )

    def scrap_login(self, response):
        other = execjs.compile('''
                function setCookie(t) { 
                    var list = t.split("; ");
                    cookie = '' 
                    for (var i = list.length - 1; i >= 0; i--) { 
                        var cname = list[i].split("=")[0]; 
                        var cvalue = list[i].split("=")[1]; 
                        var d = new Date(); 
                        d.setTime(d.getTime() + (7*24*60*60*1000)); 
                        var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); 
                        cookie += cname + "+" + cvalue + "; " + expires+"~"; 
                        } 
                    return cookie    
                    }  
                 ''')
        cookie = other.call('setCookie', coo)
        cookies = cookie.split('~')
        cookies.pop(-1)
        dict_cookie = {}
        for item in cookies:
            key_value = item.split('+')
            dict_cookie[key_value[0]] = key_value[1]

        yield scrapy.FormRequest.from_response(
            response=response,
            url='https://mobile.facebook.com',
            headers='',
            meta={'proxy': 'http://:1080'},
            cookies=dict_cookie,
            callback=self.after_login,
            dont_filter=True

        )

    def login(self, response):  # 调用splash的SplashFormRequest，提交表单参数

        yield SplashFormRequest.from_response(
            response=response,
            url=self.login_url,
            endpoint='execute',
            formdata={
                'user_agent': '',
                'cookie': ''
            },
            args={
                'wait': 30,
                'lua_source': lg,
                'proxy': 'http://:1080',
                'search_key': self.search_key
            },
            callback=self.after_login,
            errback=self.error_parse,
        )

    def parse(self, response):  # parse 方法， 暂时不考虑作用
        print(response.text)

    def after_login(self, response):  # facebook登录、搜索之后执行，此处或此处之后作为处理搜索用户html文本的方法
        # content = json.loads(response.text)
        # people_result = del_serach_result.del_people(content['1'])
        # public_result = del_serach_result.del_public(content['2'])
        # print(people_result)
        # print(public_result)

        # print(response.text)
        # for key, value in response.items:
        #     print(key)
        with open('facebook.html', 'w', encoding='utf-8') as ff:
            ff.write(response.text)
            ff.close()
        cookie = str(response.text).replace('[', '').replace(']', '')
        print(cookie)
        print(type(cookie))
        yield scrapy.FormRequest.from_response(
            response=response,
            url='https://www.facebook.com',
            headers='',
            formdata={
                'user_agent': '',
            },
            meta={'proxy': 'http://:1080'},
            cookies=cookie,
            callback=self.after_cookie,
            dont_filter=True

        )

    def error_parse(self, response):  # 登录报错执行
        pass

    def after_cookie(self, response):
        with open('facebook.html', 'a', encoding='utf-8') as ff:
            ff.write(response.text)
            ff.close()
