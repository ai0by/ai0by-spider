# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re,os
def getPageUrl(cate,num):
    url = 'https://www.mm131.net/'+cate
    response = requests.get(url,headers=headers)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text,'html.parser')
    endPage = 0
    for i in soup.find('dl',{'class':'public-box'}).find_all('dd'):
        try:
            i.find('img').get('src')
        except Exception as e:
            for s in i.find_all('a'):
                endPage = s.get('href')
            endPage = rex('list_%s_(\d+).html'%num,endPage)
            continue
        getSingleData(i.find('a').get('href'))
    for i in range(int(endPage)-1):
        nextUrl = "%s/list_%s_%s.html"%(url,num,i+2)
        response = requests.get(nextUrl, headers=headers)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in soup.find('dl', {'class': 'public-box'}).find_all('dd'):
            try:
                i.find('img').get('src')
            except Exception as e:
                continue
            getSingleData(i.find('a').get('href'))
def getSingleData(url):
    imgId = rex('.*/(\d+).html',url)
    response = requests.get(url,headers=headers)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text,'html.parser')
    title = soup.find('div',{'class':'content'}).find('h5').text
    # imgUrl = soup.find('div',{'class':'content'}).find('div',{'class':'content-pic'}).find('img').get('src')
    str1 = soup.find('div',{'class':'content-page'}).find('span').text
    imgNum = rex('共(\d+)页',str1)
    print('当前: %s 共 %s 张' % (title,imgNum))
    isExists = os.path.exists('./img/' + title)
    if not isExists:
        os.makedirs('./img/' + title)
        path = './img/' + title
    else:
        print('当前图包已存在，已自动过滤')
        return
    downImg(imgId,imgNum,path)
def downImg(imgId,imgNum,path):
    url = 'https://img1.mm131.me/pic/%s/'% imgId
    for i in range(int(imgNum)):
        imgurl = "%s%s.jpg"%(url,str(i+1))
        print(imgurl)
        try:
            print('正在下载第 %s 张' % str(i+1))
            r = requests.get(imgurl,headers=headers)
        except Exception as e:
            print('图片获取失败')
        with open('%s/[Sbcoder]_%s.jpg'%(path,i+1), 'wb') as f:
            f.write(r.content)
def rex(regexStr,str1):
    reMatch = re.match(regexStr, str1)
    return reMatch.group(1)
if __name__ == '__main__':
    print('本程序来源 20发福利资源网 www.20fa.vip')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': "http://www.mm131.com/xinggan/4995.html",
    }
    list = {'xinggan':6,'qingchun':1,'xiaohua':2,'chemo':3,'qipao':4,'mingxing':5}

    for key in list:
        getPageUrl(key,list[key])
    # getSingleData('https://www.mm131.net/xinggan/4995.html')