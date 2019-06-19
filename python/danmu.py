import requests
from bs4 import BeautifulSoup
import datetime
import mysql_engine



url=r'https://api.bilibili.com/x/v1/dm/list.so?oid=92619209'

r=requests.get(url)#访问url
r.encoding='utf8'



soup=BeautifulSoup(r.text,'lxml')#lxml是常用的解析器，需要提前使用pip工具安装lxml库
d=soup.find_all('d')#找到所有页面的d标签



dlst=[]
n=0
for i in d:
    n+=1
    danmuku={}#将单条数据装进字典
    danmuku['弹幕']=i.text
    # danmuku['弹幕']=i.attrib
    print(i["p"])
    danmuku['网址']=url
    danmuku['时间']=datetime.date.today()#需要先导入datetime库
    dlst.append(danmuku)#将所有字典装进一个列表
    print('获取了%i条数据' %n)
print(dlst)

https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp.format("78830153")