# -*- coding:utf-8 -*- 
# Author: Roc-J

import urllib
import urllib2
import re
import cookielib


class Taobao:

    # 初始化方法
    def __init__(self):
        # 登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        self.proxyURL = "http://120.193.146.97:843"
        self.loginHeaders = {
            'Host': 'login.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': 'https://login.taobao.com/member/login.jhtml?',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive'
        }

        # 用户名
        self.username = '646481338@qq.com'

        self.ua = '095#6ULo6EodR0CocERZoooooPLeIerLsPC5eFNEzPOli/uEGfcnUIc5GpYdCdcWKpbXoia7qPAXIBa7KfaxUZ67gfIwh865KtYRoRF5bAr7WL+zLjHCPCfJzLISfPY9qVH9anDLWELojpWLO+fOpSOItwETyKBhbPcYcnGqWSDfceMfoIotNObp1tpTcRR30odA84yLT7Ekclqmc7Y9bRwRoRQ5b1+eN3i9bRSfLJOV69/gbdOEy8qkbMRQDbwRoRQ5b5PeImi9bRSjEJOV69/gbdOEy8qkbMRQDtYRoRO5HAr7WPUJLjHCPC0h/OOqaxFkqVGHoIoLTnDsYVYRoRO5HWr7W2/iLjHCPC0h/OOqaxFkqVGfoIoaNp1p1tMSMyR30odoz2AAuWYVcqqmvoLoPPDoCZImZSDLvRJJ1twRooIdck7xnELoAPWAO+aUAfTOGU/Xy8LhfMaKCISLnELoAPWLO+aJBkTOGU/Xy8LhfMaKCISLnELoAPWAO+aJmjTOGU/Xy8LhfMaKCISLnELoAPWLO+fvrjTOGU/Xy8LhfMaKCISL3oLoRPC9gfuNoIoONOap1IjmYUb4jdKj/pyt6aQyPTIHoIoKNOGk1RU+ceI9IL+7uMD4jeC9cQHk87QyKvfuoIo6ceg31C5+ceO2xELo0pDjdJM6ZSDA2CQRooF9bxneo9i9bTMuoIo6ceY+1oR+ceb6PELoRPCkgfCfoIoLcebMiuERooIQCkh//oLojPZlNrfC3mQZRyFCwyGsjwW/Dolzjueu0ghRo0i9g7r7TSWPcLbBZcQ7sWosffQ3W2Ywax/t6SdYW8aMuaOyCDQ7sWosffQ53pX7fdIRooY0oA6rLdQjoIoCAS/PTb85pIFuoIoQcebp1m1+TTI9bAg7Z9ieenDLaJa+ZScLcebf1m1+c6w9bAg7Z9ie30wRooY9bar7Z9BHoIoLTnDsYQQRooF9bxZeE3i9bCuHoIoLTnDsYywRoRQ5b+4e3oo9bPDP8rOV69/gInHkySKJfxAQDYhRoRI5bAr7HnsnAv/g6QKUNAFWfxLTURwRoRQ5b5+eJmi9bRwZ+ZOV69/gbdOEy8qkbMRQDbwRoow9bBvevvi9bRw34ZfHoIoLTnDsYywRoow9b43eW9i9bRww0ZfHoIoLTnDsYVYRoRO5HAr7W2z7LjHCPC0h/OOqaxFkqVGfoIoaNm6p1tM4lbR30odoz2AAuWYVcqqmWELojpWLa+fOpTOItwETyKBhbPcYcnGqWSDfceMfoIotNObp1tbcHyR30odA84yLT7Ekclqmc7Y9b6YRoRF5bAr7WTeULjHCPCfJzLISfPY9qVH9anDLWELojpWLO+fOSOEItwETyKBhbPcYcnGqWSDfceMfoIotNObp1tbNfRR30odA84yLT7Ekclqmc7Y9b6YRoRF5bAr7WT+MLjHCPCfJzLISfPY9qVH9anDLvoLojnWv+JpmZSDLvNk61MMztPAaupqRqPWfTAh3'
        self.password2 = '9501471168bb8e6b3aa1ed9e3a421ac9336c6518ae14d7d922d8ef87b6c8549d7e2dcb27e4e794d5bafedb032884228a5412d5cfc0661d49e4239c4dbdcdeaeefd2ae3fecb519f45c06174296309fb2c233f894d16ce714b73753aec9cb6424fb48a4eda66aa453c18332251fa5a6086488fab3f207ae1ddf4c63350995ba69b'
        self.post = {
            'TPL_username': self.username,
            'TPL_password:': '',
            'ncoSig':'',
            'ncoSessionid': '',
            'ncoToken': '410f3ca5f262774b4f53e21f5cebe3a4ec2030f4',
            'slideCodeShow' :'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': '0',
            'newlogin': '0',
            'TPL_redirect_url': '',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'keyLogin':'false',
            'qrLogin':'true',
            'newMini': 'false',
            'newMini2':'false',
            'tid':'',
            'loginType':'3',
            'minititle':'',
            'minipara':'',
            'pstrong':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'sub_jump':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding':'',
            'sub':'',
            'TPL_password_2':'4a77275f01cb8d3311fd02c2554edb356d3634c904dfb9cfc0a4703f3f4e068735b2bdcbb02814f74f99b2cc095f893c60af16733c12f39168daed85be8b0c63cb2ecba3f3d2e30988496b8f5c77f4d102a784ea205fa1ad0290d31daf2c306ab596e4a3cc943baca274489d9311ffec10a073c0e9ee38d40cd94bb3ef065476',
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh - CN',
            'sr':'1280 * 1024',
            'osVer':'',
            'naviVer':'chrome | 59.03071115',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'osPF':'Win32',
            'miserHardInfo':'',
            'appkey':'',
            'nickLoginLink':'',
            'mobileLoginLink':'https://login.taobao.com/member/login.jhtml?useMobile=true',
            'showAssistantLink':'',
            'um_token':'HV01PAAZ0b871ed07b7a174d59676f5e0029d2c3',
            'ua':'095#6ULoUwoEoqoocERZoooooPLeIerLsPo5i8uEQPEli/uEGpcnUIc5qPYdCdNwKpbXoB67qPAXoBa7KfOSUZ67gpCwh865/6YRoRF5bAr7ZUuPLjHCPCfJzLISfPY9qVH9anDLWELojpWLO+a+P4HItwETyKBhbPcYcnGqWSDfceMfoIotNObp1miTZyR30odA84yLT7Ekclqmc7Y9b6wRooIdck7xnELoAPWAO+O6wjTOGU/nW2xhI0sACoSL3oLoRPC9gfCHoIoKNOZW125+ceI9Oo27uMD4jeHWCCKlsFOEKvfuoIomNOGb1A5+cea/PEdXzpRK2OTm65I5/7MuoIo6cefl1cU+ceM8PELoRPCkgfCfoIoLcebMi6wRooIdck7xqoLoR0EngxwFoIojoERMpUTqRELo0RH4oSLKkUZ90ELouPDLO+a+ZSPLcebf1m1+cWo9bAg7Z9iSbPDLaJa+ZSMHcebf1m1+c6dBoIowckyp1pT5ISbLZ3SKcgtI2aWq65MkTAY8jMHiX6K7OxWaCMvKcgtI2aWqNte5sas4/oLo0nKod+fRLRaQGyi/oIojceUp1m1+xELo0pDA6+M/ZSDLOQQRooF9bePeKmi9bMluoIomNOZY1jA+ceOcPEdXzpRK2OTm65I5/7MfoIotNObp1miTuRR30odA84yLT7Ekclqmc7Y9b6wRooIdck7xWELojpWLO+a+PGYItwETyKBhbPcYcnGqWSDfceMHoIoLTnDsYVYRoRF5bAr7ZhkMLjHCPCfJzLISfPY9qVH9anDLWELojpWLO+a+PE/ItwETyKBhbPcYcnGqWSDfceMfoIotNObp1mBrkbR30odA84yLT7Ekclqmc7Y9b6YRoRF5bAr7Z5RrLjHCPCfJzLISfPY9qVH9anDLWELojpWLO+a+FmHItwETyKBhbPcYcnGqWSDfceMfoIotNObp1mipbyR30odA84yLT7Ekclqmc7Y9bo=='
        }
        # 将POST的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        # 设置代理
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
        # 设置cookie
        self.cookie = cookielib.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler, self.proxy, urllib2.HTTPHandler)

    # 得到是否需要输入验证码，这次请求的相应有时不同，有时需要验证有时不需要
    def needIdenCode(self):
        # 第一次登录获取验证码尝试
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        response = self.opener.open(request)

        content = response.read().decode('gbk')
        print content

        status = response.getcode()

        if status == 200:
            print u"获取请求成功"
            # \u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801', re.S)
            result = re.search(pattern, content)
            # 如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                return content
            # 否则不需要
            else:
                print u"此次安全验证通过，您这次不需要输入验证码"
                return False
        else:
            print u"获取请求失败"

            # 得到验证码图片

    def getIdenCode(self, page):
        # 得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"', re.S)
        # 匹配的结果
        matchResult = re.search(pattern, page)
        # 已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False

            # 程序运行主干

    def main(self):
        # 是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needIdenCode()
        if not needResult == False:
            print u"您需要手动输入验证码"
            idenCode = self.getIdenCode(needResult)
            # 得到了验证码的链接
            if not idenCode == False:
                print u"验证码获取成功"
                print u"请在浏览器中输入您看到的验证码"
                webbrowser.open_new_tab(idenCode)
            # 验证码链接为空，无效验证码
            else:
                print u"验证码获取失败，请重试"
        else:
            print u"不需要输入验证码"


taobao = Taobao()
taobao.main()
