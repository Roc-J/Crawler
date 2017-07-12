# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib2
import cookielib

# 设置保存cookie的文件，同级目录下的cookie.txt
filename = 'Cookie.txt'

# 声明一个MozilllaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)

# 后面的基本和cookie的一样，通过urllib2来构建一个cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)

# 通过handler来构建一个opener
opener = urllib2.build_opener(handler)

# 创建一个请求
response = opener.open("http://cn.bing.com")

cookie.save(ignore_expires=True,ignore_discard=True)
