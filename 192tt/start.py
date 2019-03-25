# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import config

def getSingleData(url,i = 1):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    imgUrl = soup.find(id = 'p').find('center').find('img').get('lazysrc')
    print imgUrl
    try:
        j = i + 1
        result = '_%s.html'%i in url
        if result:
            nextImg = response.url.replace('_%s.html'%i, '_%s.html'%j)
        else:
            nextImg = response.url.replace('.html', '_%s.html'%j)
        # print nextImg
        downImg(nextImg,i)
        getSingleData(nextImg,j)
    except Exception,e:
        return 0
def getPage(url,new = 1,i = 1):
    print '开始采集第%s页'%i
    print url
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    for dataUrl in soup.find('div',{'class':'piclist'}).find('ul').find_all('li'):
        singleDataUrl = 'https://www.192tb.com/'+dataUrl.find('a').get('href')
        print singleDataUrl
        try:
            singleTitle = dataUrl.find('a').find('img').get('alt')
        except Exception,e:
            continue
        print singleTitle
        getSingleData(singleDataUrl)
    result = '_%s.html' % i in url
    j = i + 1
    if new != 1:
        nextPageUrl = url.replace('listinfo-1-%s.html' % i, 'listinfo-1-%s.html' % j)
    else:
        if result:
            nextPageUrl = url.replace('index_%s.html' % i, 'index_%s.html' % j)
        else:
            nextPageUrl = url.replace(url, url+'/index_%s.html' % j)
    getPage(nextPageUrl,new,j)
def downImg(img,m):
    r = requests.get(img)
    with open('./img/good%s.jpg' % m, 'wb') as f:
        f.write(r.content)
if __name__ == '__main__':
    url = "https://www.192tb.com//meitu/85688.html"
    print '请输入需要爬取的页面 1.美图 2.国产'
    s = input()
    if s == 1:
        getPage(config.mt,0)
    elif s == 2:
        getPage(config.gc)
    # getSingleData(url)