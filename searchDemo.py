# -*- coding:utf-8 -*- 
# Author: Roc-J


import re

print '########re.search###########'
pattern = re.compile(r'world')
match = re.search(pattern,'hello world!')
if match:
    print match.group()

print '###### re.split() ########'
pattern = re.compile(r'\d+')
print re.split(pattern,'one1two2three3four4five5ten10hundred100')


print '##### re.findall #########'
pattern = re.compile(r'\d+')
print re.findall(pattern,'one1two2three3four4five5ten10hundred100')

print '###### re.finditer #######'
pattern = re.compile(r'\d+')
for m in re.finditer(pattern,'one1two2three3four4five5ten10hundred100'):
    print m.group()


print '###### re.sub ########'
pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.sub(pattern,r'\2 \1', s)

def func(m):
    return m.group(1).title() + ' ' + m.group(2).title()

print re.sub(pattern,func,s)

print '####### re.subn(pattern,repl,string[,count) ##########'
pattern = re.compile(r'(\w+) (\w+)')
s = 'hello roc, hello world!'

print re.subn(pattern,r'\2 \1',s)

def func(m):
    return m.group(1).title() + ' '+ m.group(2).title()

print re.subn(pattern,func,s)