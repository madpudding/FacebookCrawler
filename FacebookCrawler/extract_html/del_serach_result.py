# !usr/env/bin python 3.6
# -*- coding: utf-8 -*-
# author fcj
# time 2019-01-17
# description facebook搜索结果处理
import json
from lxml import etree


def del_people(people_html):  # 处理用户html文本

    html_content = etree.HTML(people_html)
    people_url = html_content.xpath('//a[@class="_2ial"]/@href')
    people_img = html_content.xpath('//a[@class="_2ial"]/img/@src')
    single_peoples = html_content.xpath('//div[@class="_glj"]')
    print(len(single_peoples))
    people_name = html_content.xpath('//a[@class="_32mo"]/span/text()')
    peoples = {}

    for index, name in enumerate(people_name):
        peoples[name] = {'id': people_url[index], 'image_url': people_img[index]}

    for one_person in single_peoples:
        person_name = one_person.xpath('/div[@class="clearfix"]/div/div/div/div/a[@class="_32mo"]/span/text()')
        print(person_name)

    return peoples


def del_public(public_html):  # 处理公共主页html文本

    html_content = etree.HTML(public_html)
    people_url = html_content.xpath('//a[@class="_2ial"]/@href')
    people_img = html_content.xpath('//a[@class="_2ial"]/img/@src')
    people_card = html_content.xpath('//div[@class="_52eh _5bcu"]/div')

    peoples = {}

    for index, one_people in enumerate(people_card):
        name = ''.join(one_people.xpath('a[@class="_32mo"]/span/text()'))
        v = one_people.xpath('a[@class="_32mo"]/span/span')

        if len(v) > 0:
            peoples[name] = {'id': people_url[index], 'image_url': people_img[index], 'is_identify': 'Yes'}
        else:
            peoples[name] = {'id': people_url[index], 'image_url': people_img[index], 'is_identify': 'No'}

    return peoples


if __name__ == '__main__':
    with open('C:/Users/pudding/FacebookCrawler/facebook.html', 'r', encoding='utf-8') as ff:
        content = json.loads(''.join(ff.readlines()))
    user_html = content['1']
    del_people(user_html)
