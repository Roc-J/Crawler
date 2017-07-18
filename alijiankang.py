# -*- coding:utf-8 -*-
# Author: Roc-J

import urllib
import urllib2
import re
import thread
import time

# 阿里健康
class AlijiankangCrawler:

    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = { 'User-Agent': self.user_agent }
        self.matchString = '<div class="J_TItems">(.*?)<div class="pagination">'

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = u'https://maiyao.liangxinyao.com/category.htm?search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498&pageNo=' + str(pageIndex) + '#anchor'
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('gbk')
            print pageCode
            print '====================='
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接阿里健康失败，错误的原因", e.reason
                return None

     # 根据一个具体商品的URL来获取商品的详细信息
    def getProduct(self, url_goods):
        try:
            url = url_goods
            # 构建请求的request
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('gbk')
            print pageCode
            print '====================='
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接阿里健康失败，错误的原因", e.reason
                return None

    # 传入某一页代码，返回药名和URL连接
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        matchstring = '<a class="item-name J_TGoldData".*?href="(.*?)">'
        pattern = re.compile(matchstring, re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储个药物的URL链接和名称
        pageStories = []
        # 遍历正则表达式匹配的信息
        for item in items:
            # item[0]是URL，item[1]是名称
            pageStories.append([item[0].strip()])
        print pageStories
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

spider = AlijiankangCrawler()
spider.getProduct("https://detail.liangxinyao.com/item.htm?id=544499905844&rn=b0cbddc6f14ab8bf92912f3927f0d2b7&abbucket=19&skuId=3281437797774")