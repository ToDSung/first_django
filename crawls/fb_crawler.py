# -*- coding: utf-8 -*-

import facebook
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import pandas as pd

from .models import FanPage

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    
    #print file.text #to test the TOKEN
    return result

def fb_crawler(id,fan_page_name):
    
    token = 'EAACEdEose0cBANLXeRZBYjkqSVjBCl5P3XOoDaRBvKpSE9dGwg2ZA0P5MvF3pE4tbWhq5uoWwp695EvPjLQepJvMZCGZAxBSH6KQxGgxFZAAU9rGcNwLomHt192ZC9rvTv4xoTAZBsCZCj5VWIMHFWkjCqSZAW3vkf1wfij8EDsmlg0ZBwdYp4crLIZCDNoSSvAftjpNvkjNMsE0kGRnpJ5it5PSVMMRoYgnKAZD'

    graph=facebook.GraphAPI(access_token=token)

    fanpage_info = graph.get_object(str(fan_page_name), filed='id')

    fanpages = { fanpage_info['id']: fanpage_info['name']}
    # 建立一個空的list        

    information_list = []

    # 使用for迴圈依序讀取粉絲頁的資訊，並使用format將id與token傳入{}裡

    for fanpage_id in fanpages:
        res = requests.get('https://graph.facebook.com/v2.12/{}/posts?limit=100&access_token={}'.format(fanpage_id, token))
        
        # API最多一次呼叫100筆資料，因此使用while迴圈去翻頁取得所有的資料
        
        pages = 1  # 初始化爬取頁數
        
        while pages < 10: 
            print('目前正在爬取 {} {} 第{}頁'.format(fanpage_id, fanpages[fanpage_id], pages))
            for information in res.json()['data']:
                if 'message' in information:
                    
                    #res2=requests.get('https://graph.facebook.com/{}/likes?summary=true&access_token={}'.format(information['id'], token))
                    #article_likes=res2.json()['summary']['total_count']
                    
                    information_list.append([information['message'], parse(information['created_time']).date()])
                    #information_list.append([fanpages[fanpage_id], information['message'], parse(information['created_time']).date(), article_likes])
            # 若有下一頁，則繼續爬取，否則跳出While迴圈

            if 'next' in res.json()['paging']:
                res = requests.get(res.json()['paging']['next'])
                pages += 1
            else:
                print('{} {} 已爬取完成! \n'.format(fanpage_id, fanpages[fanpage_id]))
                break
            return information_list
