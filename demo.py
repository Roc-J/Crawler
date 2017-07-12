import urllib2

request = urllib2.Request("http://cuiqingcai.com/954.html")
response = urllib2.urlopen(request)
print response.read()