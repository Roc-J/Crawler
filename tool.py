# -*- coding:utf-8 -*- 
# Author: Roc-J

import re

# 工具类，主要是过滤处理页面标签
class Tool:
    # 去除img标签，空格
    removeImg = re.compile('<img.*?> | {1,7}| &nbsp;')
    # 删除超链接
    removeAddr = re.compile('<a.*?> | </a>')
    # 换行符 换\n
    replaceLine = re.compile('<tr> | <div> | </div> | </p>')
    # 表格制表<td>换 \t
    replaceTD = re.compile('<td>')
    # 换行符替换 \n
    replaceBR = re.compile('<br><br> | <br>')
    # 其余的标签删除
    removeOther = re.compile('<.*?>')
    # 将多行空行删除
    removeNoneLine = re.compile('\n+')
    def replace(self,x):
        x = re.sub(self.removeImg, '', x)
        x = re.sub(self.removeAddr, '', x)
        x = re.sub(self.replaceLine, '\n', x)
        x = re.sub(self.replaceTD, '\t', x)
        x = re.sub(self.replaceBR, '\n', x)
        x = re.sub(self.removeOther, '', x)
        x = re.sub(self.removeNoneLine, '', x)
        return x.strip()

