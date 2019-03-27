# -*-coding:utf-8 -*-
# import requests
#
# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
#
#            'AppleWebKit/537.36 (KHTML, like Gecko) '
#
#            'Chrome/56.0.2924.87 Safari/537.36'}
#
# proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}
#
# url = 'https://www.instagram.com/accounts/login/'
#
# response = requests.get(url, headers=headers, proxies=proxies)
#
# print(response.content)
# print(response.status_code)


# import requests
# from urllib.parse import quote
#
# lua = '''
# function main(splash)
#     splash:go("https://blog.csdn.net/")
# end
# '''
# proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}
# url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
# response = requests.get(url)
# print(response.content)

# import requests
#
#
# def splash_render(ul):
#     splash_url = "http://localhost:8050/render.html"
#
#     args = {
#         "url": ul,
#         "proxy": 'http://http://:1080'
#     }
#
#     response = requests.get(splash_url, params=args)
#     return response.status_code
#
#
# if __name__ == '__main__':
#     url = "https://www.facebook.com/login"
#
#     html = splash_render(url)
#     print(html)


# from scrapy_splash import SplashRequest, SplashFormRequest
#
# lua_source = '''
# function main(splash, args)
#   assert(splash:go(args.url))
#   assert(splash:wait(0.5))
#   return {
#     html = splash:html(),
#     png = splash:png(),
#     har = splash:har(),
#   }
# end
# '''
#
#
# def splash():
#     yield SplashRequest(
#         url='https://www.facebook.com/login',
#         endpoint='execute',
#         args={
#             'lua_source': lua_source,
#             'proxy': 'http://:1080',
#         },
#         callback=parse
#     )
#
#
# def parse(response):
#     print('---------')
#     print(response.text)
#
#
# if __name__ == '__main__':
#     splash()
#     splash()
import json
if __name__ == '__main__':
    with open('C:/Users/FacebookCrawler/facebook.html', 'r', encoding='utf-8') as ff:
        content = json.loads(''.join(ff.readlines()))
    user_html = content['1']

    with open('test_html.html', 'w', encoding='utf-8') as fw:
        fw.write(content['1'])
        fw.close()
    # print(content.keys())
    # print(content['1'])


