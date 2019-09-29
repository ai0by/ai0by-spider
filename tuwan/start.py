# -*- coding: utf-8 -*-
import requests
import json
import base64
import os

class Tuwan:
    def getData(self,url):
        headers = {
            "Host": "api.tuwan.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        response = requests.get(url,headers=headers)
        pageData = response.text.strip()[1:-1]
        pageData = json.loads(pageData)
        title = pageData['title']
        total = pageData['total']
        imgData = pageData['thumb']
        for i in range(len(imgData)):
            imgData[i] = imgData[i].split('/')
            imgData[i][6] = base64.b64encode(base64.b64decode(imgData[i][6].encode('utf-8')).replace('158','0'))
            joinstr = '/'
            str = joinstr.join(imgData[i])
            imgData[i] = str
        tuwan.downImg(title,total,imgData)
    def downImg(self,title,total,imgData):
        print ('当前图包:%s 共 %s 张'%(title,total))
        isExists = os.path.exists('./'+title)
        if not isExists:
            os.makedirs('./'+title)
        else:
            print ('当前资源已存在，自动跳过')
            return
        for i in range(len(imgData)):
            try:
                print ('正在下载第 %s 张' % i)
                r = requests.get(imgData[i])
            except Exception as e:
                print ("图片获取失败")
                return
            with open('./%s/[Sbcoder]_%s.jpg'%(title,i+1), 'wb') as f:
                f.write(r.content)
        return
if __name__ == '__main__':
    tuwan = Tuwan()
    print ('本程序由风向标博客提供 sbcoder.cn')
    print ('请输入起始ID')
    startId = int(input())
    print ('请输入结束ID')
    endId = int(input())
    while startId < endId:
        try:
            url = 'https://api.tuwan.com/apps/Welfare/detail?id=%s'%startId
            tuwan.getData(url)
            startId = startId + 1
        except Exception as e:
            print ('当前ID错误:%s'% startId)
            print (e)