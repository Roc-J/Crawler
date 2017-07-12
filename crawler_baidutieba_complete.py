# -*- coding:utf-8 -*- 
# Author: Roc-J

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

    # 初始化，传入基地址，是否只看楼主的参数，显示楼层分隔符
    def __init__(self, baseUrl, seeLZ, floorTag):
        # base连接地址,参数传入
        self.baseURL = baseUrl
        # 是否只看楼主
        self.seeLZ = '?see_lz=' + str(seeLZ)
        # 剔除标签
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 给出默认的标题，如果没有成功获取到标题的话，就使用这个标题
        self.defaultTitle = u"百度贴吧"
        # 是否写入楼分割符的标记
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            # print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败，错误的原因是"
                print e.reason
                return None

    # 提取帖子标题
    def getTitle(self, page):
        matchstring = '<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>'
        pattern = re.compile(matchstring, re.S)
        result = re.search(pattern, page)
        if result:
            # print '帖子标题:', result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 获取帖子一共有多少页
    def getPageNum(self, page):
        matchstring = '<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>'
        pattern = re.compile(matchstring, re.S)
        result = re.search(pattern, page)
        if result:
            # print '帖子页数:',result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 获取每一层楼的内容。传入页面内容
    def getContent(self, page):
        matchsting = '<div id="post_content_.*?>(.*?)</div>'
        pattern = re.compile(matchsting, re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        # 如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + '.txt','w+')
        else:
            self.file = open(self.defaultTitle + '.txt','w+')

    def writeData(self,contents):
        # 向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                # 加一个楼的分割符
                floorLine = '\n' + str(self.floor) + u'---------------------------------------------------\n'
                self.file.write(floorLine)
                self.floor += 1
            self.file.write(item)

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL已经失效，请重试'
            return
        try:
            print '该帖子共有' + str(pageNum) + '页'
            for i in range(1, int(pageNum)+1):
                print '正在写入第'+ str(i) + '页数据'
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print '写入异常，原因' + e.message
        finally:
            print '写入任务完成'


print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/\n'))
seeLZ = raw_input('是否只获取楼主发言，是输入1，否输入0\n')
floorTag = raw_input('是否写入楼层信息，是输入1，否输入0\n')

bdtb = crawler_BDTB(baseURL, seeLZ, floorTag)
bdtb.start()