# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import thread
import time

# 糗事百科爬虫
class QSBKCrawler:

    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = { 'User-Agent': self.user_agent }
        self.matchString = '<div.*?clearfix">.*?<a.*?<img.*?<h2(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?' + \
              '<div.*?stats">.*?<span.*?stats-vote">.*?<i.*?number">(.*?)</i>.*?' + \
              '<span.*?stats-comments">.*?<a.*?<i.*?number">(.*?)</i>'

        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []

        # 存放程序是否继续的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接糗事百科失败，错误的原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile(self.matchString,re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储每页的段子
        pageStories = []
        # 遍历正则表达式匹配的信息
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item[1])
            # item[0]是段子的发布者，item[1]是内容，item[2]是好笑数，item[3]是评论数
            pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories

    # 加载并提取页面的内容，并加入列表中
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                # 获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人: %s\t 好笑数: %s\t 评论数: %s\n%s" % (page,story[0],story[2],story[3],story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        # 使变量为True
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) >0:
                pageStories = self.stories[0]
                nowPage +=1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBKCrawler()
spider.start()