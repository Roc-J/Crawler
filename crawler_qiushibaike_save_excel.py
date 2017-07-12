# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import xlwt
import xlrd
import os
import time
from xlutils.copy import copy

class crawler_qiushibaike_save_excel:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = { 'User-Agent': self.user_agent}
        self.matchString = '<div.*?clearfix">.*?<a.*?<img.*?<h2(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?' + \
              '<div.*?stats">.*?<span.*?stats-vote">.*?<i.*?number">(.*?)</i>.*?' + \
              '<span.*?stats-comments">.*?<a.*?<i.*?number">(.*?)</i>'

    def crawler_data(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/text/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageContent = response.read().decode('utf-8')
            pattern = re.compile(self.matchString, re.S)
            items = re.findall(pattern, pageContent)
            pageStories = []
            for item in items:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, '\n', item[1])
                pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
            return pageStories
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接糗事百科出现错误",e.reason
                return None

    def save(self,pageIndex):
        pageStories = self.crawler_data(pageIndex)
        if os.path.exists("qiushibaike.xls"):
            rb = xlrd.open_workbook("qiushibaike.xls")
            sh = rb.sheet_by_index(0)
            print '行数',sh.nrows,'列数',sh.ncols
            wb = copy(rb)
            s = wb.get_sheet(0)
            row = sh.nrows
            for story in pageStories:
                # print u"第%d页\t发布人: %s\t 好笑数: %s\t 评论数: %s\n%s" % (pageIndex, story[0], story[2], story[3], story[1])
                s.write(row, 0, story[0])
                s.write(row, 1, story[1])
                s.write(row, 2, story[2])
                s.write(row, 3, story[3])
                row += 1
            wb.save('qiushibaike.xls')
        else:
            wb = xlwt.Workbook()
            sh = wb.add_sheet(u'糗事百科')
            row = 0
            for story in pageStories:
                # print u"第%d页\t发布人: %s\t 好笑数: %s\t 评论数: %s\n%s" % (pageIndex, story[0], story[2], story[3], story[1])
                sh.write(row, 0, story[0])
                sh.write(row, 1, story[1])
                sh.write(row, 2, story[2])
                sh.write(row, 3, story[3])
                row += 1
            wb.save('qiushibaike.xls')

    def start(self):
        while self.pageIndex<=35:
            self.save(self.pageIndex)
            self.pageIndex +=1
            time.sleep(2)

spider = crawler_qiushibaike_save_excel()
spider.start()