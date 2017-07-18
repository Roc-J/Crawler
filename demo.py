import urllib2

request = urllib2.Request("https://maiyao.liangxinyao.com/category.htm?search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498&pageNo=1")
response = urllib2.urlopen(request)
print response.read().decode('gbk')