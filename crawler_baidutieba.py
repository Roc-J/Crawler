# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib2
import urllib
import re

# 处理页面标签类
class Tool:
    # 去除img标签，或者7位空格
    removeImg = re.compile('<img.*?> |  {7}|')
    # 去除超链接标签
    removeAhref = re.compile('<a.*?>| </a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>换\t
    replaceTD = re.compile('<td>')
    # 把段落开头换\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或者双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    replaceOther = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAhref, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n   ",x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.replaceOther, "", x)
        return x.strip()

class crawler_BDTB:

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    # 提取帖子标题
    def getTitle(self):
        page = self.getPage(1)
        matchstring = '<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>'
        pattern = re.compile(matchstring, re.S)
        result = re.search(pattern, page)
        if result:
            print '帖子标题:', result.group(1)
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        page = self.getPage(1)
        matchstring = '<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>'
        pattern = re.compile(matchstring, re.S)
        result = re.search(pattern, page)
        if result:
            print '帖子数:',result.group(1)
        else:
            return None

    def getContent(self):
        page = self.getPage(1)
        matchsting = '<div id="post_content_.*?>(.*?)</div>'
        pattern = re.compile(matchsting, re.S)
        items = re.findall(pattern, page)
        floor = 1
        for item in items:
            print floor,u'楼---------------------------------------------------------------------------------------------------------\n'
            print self.tool.replace(item)
            floor += 1

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = crawler_BDTB(baseURL,1)
# bdtb.getTitle()
bdtb.getPageNum()
# bdtb.getContent()