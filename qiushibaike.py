# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers = {'User-Agent': user_agent}

matchString = '<div.*?clearfix">.*?<a.*?<img.*?<h2(.*?)</h2>.*?<div.*?content">.*?<span>(.*?)</span>.*?' + \
              '<div.*?stats">.*?<span.*?stats-vote">.*?<i.*?number">(.*?)</i>.*?' + \
              '<span.*?stats-comments">.*?<a.*?<i.*?number">(.*?)</i>'
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile(matchString, re.S)
    items = re.findall(pattern, content)
    for item in items:
        print '用户名',item[0]
        print '内容',item[1]
        print '好笑数',item[2]
        print '评论数',item[3]
        print '\n'
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

