# -*- coding:utf-8 -*-
# Author: Roc-J
import urllib2
import cookielib

# 声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()

# 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)

# 通过handler来构建opener
opener = urllib2.build_opener(handler)

response = opener.open('http://www.baidu.com')

for item in cookie:
    print 'Name = ' + item.name
    print 'Value = ' + item.value