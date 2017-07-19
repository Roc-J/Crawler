# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import os
import xlrd
import xlwt
from xlutils.copy import copy
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import sys
import tool
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


# 阿里健康
class AlijiankangCrawler:

    # 初始化方法，定义一些变量
    def __init__(self):
        self.path = "E:/webdriver/chromedriver"
        self.driver = webdriver.Chrome(self.path)
        self.driver.set_page_load_timeout(10)
        self.driver.maximize_window()
        self.tool = tool.Tool()

    # 模拟登陆
    def simulation_load(self):
        try:
            self.driver.get('https://login.taobao.com/?style=mini&full_redirect=true&from=liangxinyao&css_style=liangxinyao&newMini2=true&enup=true&qrlogin=true&keyLogin=true&redirectURL=https%3A%2F%2Fmaiyao.liangxinyao.com%2F%3Fspm%3Da21mf.86774.393628.1.2cc9a7d9BmL8Oo')
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
            self.driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys("646481338@qq.com")
            self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys("#211qin381")
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
            time.sleep(10)
            self.driver.get("https://maiyao.liangxinyao.com/i/asynSearch.htm?_ksTS=1500288989283_137&callback=jsonp138&mid=w-15153317282-0&wid=15153317282&path=/category.htm&&search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498")
        except TimeoutException:
            print "加载的时间太长了，终止加载"
            self.driver.execute_script('window.stop()')
        time.sleep(3)

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = u'https://maiyao.liangxinyao.com/i/asynSearch.htm?_ksTS=1500288989283_137&callback=jsonp138&mid=w-15153317282-0&wid=15153317282&path=/category.htm&&search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498&pageNo=' + str(pageIndex)
            # 构建请求的request
            self.driver.get(url)
        except TimeoutException:
            print("超时停止加载页面")
            self.driver.execute_script('window.stop()')
        time.sleep(3)
        return self.driver.page_source

    # 传入某一页代码，返回药名和URL连接
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        matchstring = '<a.*?item-name.*?href.*?"(.*?)".*?>(.*?)</a>'
        # print matchstring
        pattern = re.compile(matchstring, re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储个药物的URL链接和名称
        pageURL = []
        # 遍历正则表达式匹配的信息
        for item in items:
            # item[0]是URL，item[1]是名称
            # print item[0]
            goodsURL = "https:" + item[0][7:len(item[0])-7].strip()
            # print item[1]
            goodsName = item[1]
            # pageStories.append([goodsURL, goodsName])
            pageURL.append(goodsURL)
        return pageURL[:len(pageURL)-8]

    # 根据每一条URL地址进行商品详细信息的抓取
    def getPageContent(self, goodsURL):
        try:
            self.driver.get(goodsURL)
        except TimeoutException:
            print "停止加载页面" + goodsURL
            self.driver.execute_script("window.stop()")

        print "获取到页面内容"
        contents = self.driver.page_source

        goods_list = []
        goods_list.append(goodsURL)
        # 开始进行商品详细的抓取
        match_price = '<dl class="tm-price-panel.*?<span class="tm-price">(.*?)</span>'
        pattern_price = re.compile(match_price, re.S)
        items_price = re.findall(pattern_price, contents)
        for item in items_price:
            # print "价格", item.strip()
            goods_list.append(item.strip())

        match_proprice = '<dl class="tm-promo-panel tm-promo-cur.*?<span class="tm-price">(.*?)</span>'
        pattern_proprice = re.compile(match_proprice, re.S)
        items_proprice = re.findall(pattern_proprice, contents)
        if items_proprice:
            for item in items_proprice:
                # print "促销价格", item.strip()
                goods_list.append(item.strip())
        else:
            goods_list.append("")

        # 这个需要改进
        match_service = '<ul class="tm-clear serviceList.*?<li.*?<a.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span.*?>(.*?)</span>'
        pattern_service = re.compile(match_service,re.S)
        items_service = re.findall(pattern_service, contents)
        for item in items_service:
            # print "服务", item[0],item[1],item[2]
            service = item[0] + "" + item[1] + item[2]
            goods_list.append(service)

        match_count = '<ul class="tm-ind-panel.*?<li.*?<span class="tm-count">(.*?)</span>.*?<li.*?<span class="tm-count">(.*?)</span>.*?<span id="J_CollectCount">(.*?)</span>'
        pattern_count = re.compile(match_count, re.S)
        items_count = re.findall(pattern_count, contents)
        for item in items_count:
            # print "月销量", item[0]
            # print "评价", item[1]
            # print "收藏", item[2]
            goods_list.append(item[0])
            goods_list.append(item[1])
            goods_list.append(item[2])

        matchstring = '<a class="J_EbrandLogo".*?>(.*?)</a>.*?' + \
                    '<ul id="J_AttrUL".*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>.*?' + \
                    '<li.*?>(.*?)</li>'
        pattern = re.compile(matchstring, re.S)
        items = re.findall(pattern, contents)
        for item in items:
            # item[0]是品牌名称
            # item[1]是产品名称
            # item[2]是使用剂型
            # item[3]是使用剂量
            # item[4]是品牌
            # item[5]是套餐类型
            # item[6]是有效期
            # item[7]是用法
            # item[8]是药品分类
            # item[9]药品名称
            # item[10]药品通用名
            # item[11]批准文号
            # item[12]生产企业
            # item[13]规格
            # item[14]类别
            # print item[0].strip()
            # print item[1].strip()
            # print item[2].strip()
            # print item[3].strip()
            # print item[4].strip()
            # print item[5].strip()
            # print item[6].strip()
            # print item[7].strip()
            # print item[8].strip()
            # print item[9].strip()
            # print item[10].strip()
            # print item[11].strip()
            # print item[12].strip()
            # print item[13].strip()
            # print item[14].strip()
            for i in range(15):
                goods_list.append(self.tool.strSplit(item[i].strip()))
        return goods_list

    def save(self, goods_list):
        if os.path.exists("goods.xls"):
            rb = xlrd.open_workbook("goods.xls")
            sh = rb.sheet_by_index(0)
            # print '行数',sh.nrows,'列数',sh.ncols
            wb = copy(rb)
            s = wb.get_sheet(0)
            row = sh.nrows
            for goods_item in goods_list:
                for i in range(len(goods_item)):
                    s.write(row, i, goods_item[i])
                row += 1
            wb.save('goods.xls')
        else:
            wb = xlwt.Workbook()
            sh = wb.add_sheet(u'阿里健康')
            row = 0
            for goods_item in goods_list:
                #
                for i in range(len(goods_item)):
                    sh.write(row, i, goods_item[i])
                row += 1
            wb.save('goods.xls')

    # 开始方法
    def start(self):
        self.simulation_load()
        urlLists = []
        for i in range(15, 16):
            urlList = self.getPageItems(i)
            urlLists += urlList
        urlSet = set(urlLists)
        urlLists = list(urlSet)
        print len(urlLists)

        goods_lists = []
        for url in urlLists:
            goods_item = self.getPageContent(url)
            goods_lists.append(goods_item)
            time.sleep(2)
        self.save(goods_lists)

        self.driver.close()



spider = AlijiankangCrawler()
spider.start()

