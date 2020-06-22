# -*- coding: utf-8 -*-
import requests,os
from lxml import etree
import threadpool
# edit by biezhi
Url = "https://www.moestack.com/all"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

def Mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        pass

def Get_Page(x):
    Page = requests.get(x,headers=headers)
    Page.encoding = "utf-8"
    Page = Page.text
    Page = etree.HTML(Page)
    return Page

def DownImg(title,imgUrl):
    path = "Moe/" + title + "/"
    Mkdir(path)
    for i in range(len(imgUrl)):
        print("\033[0;32m正在下载图片：%s%d/%d\033[0m"%(title,i+1,len(imgUrl)))
        ImgUrl = imgUrl[i]
        save_img = requests.get(ImgUrl, headers=headers)
        with open(r"Moe/" + title + "/" + str(i+1) + ".jpg", "wb") as fh:
            fh.write(save_img.content)
            fh.flush()
    print("\033[0;32m下载完成\033[0m")

def OnePageDown(x):
    GetImgUrl = Get_Page(x).xpath('//*/div[2]/div/div[1]/p/img/@src')
    Title = Get_Page(x).xpath('//*[@class="entry-title"]/text()')
    print("标题：" + Title[0])
    DownImg(Title[0],GetImgUrl)

def PageDown(x):
    ImgPageUrl = Get_Page(x).xpath('//*[@class="entry-media"]/div/a/@href')
    for i in ImgPageUrl:
        OnePageDown(i)

def AllDown(x):
    PageNum = Get_Page(x).xpath('/html/body/div/div[3]/div/div[2]/div/div/main/div[2]/ul/li[6]/a/text()')
    print("全站共有%d页"%int(PageNum[0]))
    pool = threadpool.ThreadPool(Speed)
    list = []
    for i in range(int(PageNum[0])):
        i = i + 1
        if i == '1':
            PageUrl = "https://www.moestack.com/all"
            list.append(PageUrl)
            # PageDown(PageUrl)
        else:
            PageUrl = "https://www.moestack.com/all" + "/page/" + str(i)
            list.append(PageUrl)
            # PageDown(PageUrl)
    pageTask = threadpool.makeRequests(PageDown, list)
    [pool.putRequest(req) for req in pageTask]
    pool.wait()

def main():
    print("\033[0;36mAuthor biezhi edit by sbcoder.cn \033[0m")
    print("\033[0;36m菜单：\n1.单页下载\n2.页面下载\n3.全站下载(Boom!!!)\n图源来自 https://www.moestack.com/\033[0m")
    Choice = input("\033[0;32m请选择：\033[0m")

    if Choice == '1':
        ImgPageUrl = input("\033[0;32m请输入链接：\033[0m")
        OnePageDown(ImgPageUrl)
    elif Choice == '2':
        PageUrl = input("\033[0;32m请输入页面链接：\033[0m")
        PageDown(PageUrl)
    elif Choice == '3':
        global Speed
        Speed = input("\033[0;32m输入最大线程数：\033[0m")
        Speed = int(Speed)
        AllDown(Url)

if __name__ == "__main__":
    main()