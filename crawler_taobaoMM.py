# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import os


class Spider:

    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        matchString = '<div class="pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<strong>(.*?)</strong>'
        pattern = re.compile(matchString, re.S)
        items = re.findall(pattern, page)
        for item in items:
            print item[0],item[1],item[2],item[3],item[4],item[5],item[6]

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    # 写入文本
    def saveBrief(self, content, name):
        fileName = name + '/' + name + ".txt"
        f = open(fileName, "w+")
        print u"正在偷偷保存她的个人信息",fileName
        f.write(content.decode('utf-8'))

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在目录就创建目录
            os.makedirs(path)
            return True
        else:
            return False

spider = Spider()
spider.getContents(1)