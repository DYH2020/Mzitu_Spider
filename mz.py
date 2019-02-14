#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'ZYSzys'

import requests
from bs4 import BeautifulSoup
import os
import random
import time


class Mz:
    def __init__(self):
        self.url = 'http://www.mzitu.com/xinggan'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Referer': 'http://www.mzitu.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'close'
        }
        self.req = requests.session()
        self.all_a = []
        self.all_a_title = []
        self.all_a_max = []
        self.user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                                "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                                ]

        if os.access("Mzitu", os.F_OK):
            pass
        else:
            os.makedirs(os.path.join(os.getcwd(), 'Mzitu'))
        os.chdir(os.path.join(os.getcwd(), 'Mzitu'))

        self.initpwd = os.getcwd()

    # 下载html
    def Domainhtml(self, n=1):

        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        url = self.url + "/page/" + str(n)
        print(url)
        html = self.req.get(url, headers=self.headers)
        # 得到当前页面的所有li
        lis = BeautifulSoup(
            html.text, 'lxml').find('div', class_='postlist').find_all('li')
        for a in lis:
            imgurl = a.find('a')['href']
            self.all_a.append(imgurl)

        print(len(self.all_a))

    # 得到最大页
    def Getmaxpage(self):
        for a in self.all_a:
            imghtml = self.req.get(a, headers=self.headers)
            title = BeautifulSoup(imghtml.text, 'lxml').find(
                'h2', class_='main-title').string
            #print title
            last = BeautifulSoup(imghtml.text, 'lxml').find(
                'div', class_='pagenavi').find_all('span')
            last = int(last[-2].string)
            self.all_a_title.append(title)
            self.all_a_max.append(last)

    # 下载
    def Downloadimg(self):
        cnt = 0
        print('total: %s' % len(self.all_a))

        for a in self.all_a:
            print('Downloading %s now...' % (cnt+1))

            currentPwd = self.all_a_title[cnt]
            if os.access(currentPwd, os.F_OK):
                pass
            else:
                os.makedirs(os.path.join(os.getcwd(), currentPwd))

            os.chdir(os.path.join(os.getcwd(), currentPwd))
            # 随机切换User-Agent：
            self.headers['User-Agent'] = random.choice(self.user_agent_list)
            time.sleep(2)

            # 下载每张里面的图片
            for i in range(1, self.all_a_max[cnt] + 1):
                imgName = str(i)+'.jpg'

                if os.path.exists(imgName):
                    print(currentPwd+"/"+imgName+"已存在")
                else:
                    # time.sleep(1)
                    nurl = a + '/' + str(i)
                    # 超时或出错重试，三次重连机制
                    i = 0
                    while i < 3:
                        try:
                            imghtml = self.req.get(
                                nurl, headers=self.headers, timeout=(5, 10))
                            # 得到图片地址
                            aaa = BeautifulSoup(imghtml.text, 'lxml').find(
                                'div', class_='main-image').find('img')['src']
                            # 根据图片地址得到图片
                            img = self.req.get(aaa, headers=self.headers)
                            f = open(imgName, 'ab')
                            f.write(img.content)
                            f.close()
                            print(currentPwd+"/"+imgName+"下载成功")
                            i = 3
                        except requests.exceptions.RequestException as e:
                            print(e)
                            print(currentPwd+"/"+imgName+"下载失败"+'\t出错地址：'+nurl)
                            i += 1

            cnt += 1
            os.chdir(self.initpwd)

        print('Dowmload completed!')

    def GetMaxDomainHtmlPage(self):
        html = self.req.get(self.url, headers=self.headers)
        # 得到最大的页书
        max_page = BeautifulSoup(html.text, 'lxml').find_all(
            'a', class_='page-numbers')
        max_page = int(max_page[-2].string)

        for n in range(1, 2):
            time.sleep(5)
            test.Domainhtml(n)
            test.Getmaxpage()
            test.Downloadimg()
            # 下载一次之后需要将存放数据的记录都清空
            self.all_a_title = []
            self.all_a = []
            self.all_a_max = []

        print(max_page)


if __name__ == '__main__':
    test = Mz()
    test.GetMaxDomainHtmlPage()
    # test.Domainhtml()
    # test.Getmaxpage()
    # test.Downloadimg()
