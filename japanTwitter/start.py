# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random

def spy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for imgSoup in soup.find_all('div', {"class": "row"}):
        for i in imgSoup.find_all('div', {'class': 'photo'}):
            for j in i.find('div', {'class': 'photo-link-outer'}).find('a').find_all('img'):
                img = j.get("src")
                print (img)
                str = random.sample('zyxwvutsrqponmlkjihgfedcba', 6)
                downImg(img, str)
    nexturl = soup.find('p',{'class':'go-to-next-page'})
    nexturl = nexturl.find('a').get('href')
    pageurl = "http://jigadori.fkoji.com"+nexturl
    spy(pageurl)

def downImg(img,m):
    try:
        r = requests.get(img)
    except Exception as e:
        print ("图片获取失败")
        return
    with open('./img/good%s.jpg' % m, 'wb') as f:
        f.write(r.content)
if __name__ == '__main__':
    url = "http://jigadori.fkoji.com"
    spy(url)