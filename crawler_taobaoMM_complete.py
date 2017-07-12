# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import os
import tool
import time

# 抓取MM
class Spider:

    # 页面初始化
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()

    # 获取索引页面的内容
    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        # print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    # 获取页面所有MM的信息，存到list中
    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        matchString = '<div class="pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<strong>(.*?)</strong>'
        pattern = re.compile(matchString, re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            # print item[0],item[1],item[2],item[3],item[4],item[5],item[6]
            contents.append([item[0],item[1],item[2],item[3],item[4],item[5],item[6]])
        return contents

    # 获取MM个人详细页面
    def getDetailPage(self, infoURL):
        url = "https:"+infoURL
        response = urllib2.urlopen(url)
        return response.read().decode('gbk')

    # 获取个人文字简介
    def getBrief(self, page):
        matchString = '<div class="mm-aixiu-content".*?>(.*?)<!--'
        pattern = re.compile(matchString, re.S)
        result = re.search(pattern, page)
        print "个人简介",result.group(1)
        if result.group(1):
            return self.tool.replace(result.group(1))
        else:
            return None

    # 得到页面的所有图片
    def getAllImg(self,page):
        matchString = '<div class="mm-aixiu-content".*?>(.*?)<!--'
        pattern = re.compile(matchString, re.S)
        content = re.search(pattern, page)
        if content.group(1):
            # 从内容中挑选出照片
            matchImg = '<img.*?src="(.*?)">'
            imgPattern = re.compile(matchImg,re.S)
            images = re.findall(imgPattern, content.group(1))
            return images
        else:
            return None

    # 保存多张写真照片
    def saveImgs(self, images, name):
        if images:
            number = 1
            print u"发现",name,u"共有",len(images),u"张照片"
            for imageURL in images:
                splitPath = imageURL.split('.')
                fTail = splitPath.pop()
                if len(fTail) > 3:
                    fTail = "jpg"
                fileName = name + "/" + str(number) + "." + fTail
                self.saveImg(imageURL,fileName)
                number += 1

    # 保存头像
    def saveIcon(self, iconURL, name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL, fileName)

    # 保存个人简介
    def saveBrief(self,content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, "w+")
        print u"正在偷偷保存她的个人信息为",fileName
        print content
        f.write(content.encode('utf-8'))

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        imageURL = "https:"+imageURL
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在悄悄保存她的一张图片为",fileName
        f.close()

    # 写入文本
    def saveBrief(self, content, name):
        fileName = name + '/' + name + ".txt"
        f = open(fileName, "w+")
        print u"正在偷偷保存她的个人信息",fileName
        if content:
            f.write(content.decode('utf-8'))

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在目录就创建目录
            print u"偷偷新建了名字叫做",path,u"的文件夹"
            os.makedirs(path)
            return True
        else:
            print u"名为",path,'的文件夹已经创建成功'
            return False

    # 将一页淘宝MM的信息保存
    def savePageInfo(self,pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]个人详情URL,item[1]头像URL,item[2]姓名，item[3]年龄，item[4]居住地,item[5]职业，item[5]粉丝数
            print u"发现一位模特，名字叫",item[2],u"芳龄",item[3],u",她在",item[4],u",职业是",item[5],u",粉丝数有",item[5]
            print u"正在偷偷的保存",item[2],"的信息"
            print u"又意外的发现她的个人地址是",item[0]

            # 个人详情页
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            # print detailPage
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief, item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images,item[2])

    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM"
            self.savePageInfo(i)
            time.sleep(3)

spider = Spider()
spider.savePagesInfo(1,3)