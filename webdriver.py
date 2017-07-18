# -*- coding:utf-8 -*- 
# Author: Roc-J

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import time
path = 'E:/webdriver/chromedriver'
driver = webdriver.Chrome(path)
driver.set_page_load_timeout(5)
driver.maximize_window()

try:
    driver.get('https://login.taobao.com/?style=mini&full_redirect=true&from=liangxinyao&css_style=liangxinyao&newMini2=true&enup=true&qrlogin=true&keyLogin=true&redirectURL=https%3A%2F%2Fmaiyao.liangxinyao.com%2F%3Fspm%3Da21mf.86774.393628.1.2cc9a7d9BmL8Oo')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys("646481338@qq.com")
    driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys("#211qin381")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
except TimeoutException:
    print "加载的时间太长了，终止加载"
    driver.execute_script('window.stop()')

print "数据停止"
time.sleep(10)
print "数据开始"

try:
    driver.get("https://maiyao.liangxinyao.com/i/asynSearch.htm?_ksTS=1500288989283_137&callback=jsonp138&mid=w-15153317282-0&wid=15153317282&path=/category.htm&&search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498")
except TimeoutException:
    print "停止加载网页"
    driver.execute_script("window.stop()")

print "数据停止"
time.sleep(10)
print "数据开始"

try:
    print "开始打开新的URL"
    driver.get("https://maiyao.liangxinyao.com/i/asynSearch.htm?_ksTS=1500288989283_137&callback=jsonp138&mid=w-15153317282-0&wid=15153317282&path=/category.htm&&search=y&catName=%D7%CC%B2%B9%B5%F7%D1%F8&catId=1250009498&pageNo=4")
except TimeoutException:
    print("超时停止加载页面")
    driver.execute_script('window.stop()')

print "抓取的页面"
print driver.page_source