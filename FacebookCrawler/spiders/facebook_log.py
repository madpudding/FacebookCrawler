# !usr/env/bin python 3.6
# -*- coding: utf-8 -*-
# author fcj
# time 2018-12-28
# description facebook登录

import scrapy
import re
import json
import datetime
import sys
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy_splash import SplashMiddleware
from scrapy.http.request.form import Request
from scrapy import Selector
from scrapy.http.request.form import FormRequest
from scrapy.spiders.init import  InitSpider
from scrapy.exceptions import CloseSpider
from FacebookCrawler.items import FacebookPosts
from FacebookCrawler.extract_html import del_serach_result


# lua脚本
lua_script = """  
    local random = math.random
    json = require("json")
    function main(splash)
        local cookies = splash.args.headers['Cookie']
        splash:on_request(
            function(request)
                request:set_header('Cookie', cookies)
            end
        )
        splash:go{splash.args.url, headers=splash.args.headers}
        splash:wait(10)
        --png1 = splash:png{render_all=true}
        -- random wait, be more like a human
        local ok, error = splash:runjs([[window.scrollTo(0, document.body.scrollHeight/2)]])
        splash:wait(math.random(5,10))
        --png2 = splash:png{render_all=true}
        local entries = splash:history()
        -- local last_entry = entries[#entries]
        local last_response = entries[#entries].response
        return {
            url = splash.args.url,
            html = splash:html(),
            http_status = last_response.status,
            headers = last_response.headers,
            cookies = splash:get_cookies(),
            --png1 = png1,
            --png2 = png2,
            data = json.encode(updates),
            har = json.encode(splash:har()),
        }
    end
"""

#  lua设置端口脚本
port_lua_script = '''  
    function main(splash, arg)
        splash:on_request(function request()
            request:set_proxy{
                host='0.0.0.0',
                port=0,
                username='',
                password='',
                type="http",
                }
                end)
                --- do something ---
    end
'''

#  facebook lua设置登录脚本,账号密码登录用这个，需要user、password
log_lua_script = '''  
function main(splash, args)
    local ok, reason=splash:go(args.url)

    user_name=args.user_name
    user_pass=args.user_password
    user_text=splash:select('#email')
    pass_text=splash:select('#pass')
    login_btn=splash:select('#loginbutton')

    if(user_text and pass_text and login_btn) then
        user_text:send_text(user_name)
        pass_text:send_text(user_pass)
        login_btn:mouse_click({})
    end

    splash:wait(math.random(5,10))
    return {
        html = splash:html(),
        }
end
'''

user = "com"  # 后续 user 和 password 应该 是读取数据库，暂时先写死在这里。
password = "a"

coo = 'datr=; fr=' \
      '; sb=; c_user=; xs=' \
      '; pl=; m_pixel_ratio=; wd='  # 用户 cookie
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
    splash:wait(math.random(3,5))
    search_key = args.search_key
    search_text = splash:select('.inputtext')
    search_btn = splash:select('button[type=submit]')

    if (search_text and search_btn) then
        search_text: send_text(search_key)
        search_btn: mouse_click({})    
    end
    splash:wait(math.random(4,5))

    user_href = splash:select('li[data-edge=keywords_users]')
    if user_href then
        user_href: mouse_hover({x=0, y=0})
        user_href: mouse_click({})

    end
    splash:wait(math.random(4,5))
    user_html = splash:html()

    public_href = splash:select('li[data-edge=keywords_pages]')
    if public_href then
        public_href: mouse_hover({x=0, y=0})
        public_href: mouse_click({})
    end
    splash:wait(math.random(4,5))
    public_html = splash:html()

    return {
    user_html,
    public_html,
    }
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
    html=splash:html(),
    }
end
'''
five = '    splash:runjs("javascript:void(function(){ function setCookie(t) { var list = t.split(\'; \');' \
       ' console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split(\'=\')[0];' \
       ' var c_value = list[i].split(\'=\')[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000));' \
       ' var expires = \';domain=.facebook.com;expires=\'+ d.toUTCString(); document.cookie = cname + \'=\' +' \
       ' c_value + \'; \' + expires; } }  var cookie = \'' + coo + '\'; setCookie(cookie); location.href =' \
       ' \'https://www.facebook.com\'; })();")'  # https://mobile.facebook.com H5页面 https://www.facebook.com 电脑web

lg = zero + '\n' + five + '\n' + zero_end


class FacebookLogSpider(scrapy.Spider):  # facebook 登录 ，scrapy_Request 登录 login页面，再在 login 调用 splash。
    name = 'facebook'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    login_url = 'https://www.facebook.com/login'  # https://www.facebook.com/login 电脑web登录
    start_urls = []
    search_key = 'Michael'

    def start_requests(self):  # 起点

        yield Request(
            url=self.login_url,
            callback=self.log_with_cookie,
            meta={'proxy': 'http://:1080'}
        )

    def login(self, response):  # 调用splash的SplashFormRequest，提交表单参数(user、password)

        yield SplashFormRequest.from_response(
            response=response,
            url=self.login_url,
            formdata={
                'email': user,
                'password': password
            },
            endpoint='execute',
            args={
                'wait': 30,
                'lua_source': log_lua_script,
                'user_name': user,
                'user_password': password,
                'proxy': 'http://:1080'
            },
            callback=self.after_login,
            errback=self.error_parse,
        )

    def log_with_cookie(self, response):  # 调用splash的SplashFormRequest，提交表单参数,使用cookie和user_agent(暂时没用到)
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
                'proxy': 'http://192.168.6.163:1080',
                'search_key': self.search_key
            },
            callback=self.after_login,
            errback=self.error_parse,
        )

    def parse(self, response):  # parse 方法
        print(response.text)

    def after_login(self, response):  # facebook登录、搜索之后执行，此处或此处之后作为处理搜索用户html文本的方法
        content = json.loads(response.text)
        people_result = del_serach_result.del_people(content['1'])
        public_result = del_serach_result.del_public(content['2'])
        print(people_result)
        print(public_result)
        # print(response.text)
        # for key, value in response.items:
        #     print(key)
        # with open('facebook.html', 'w', encoding='utf-8') as ff:
        #     ff.write(response.text)
        #     ff.close()

    def error_parse(self, response):  # 登录报错执行
        pass

