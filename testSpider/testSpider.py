#-*- coding = utf-8 -*-
#@Time : 2020/7/30 
#@Author:张家林
#@File : testSpider.py
#@Software:{PyCharm}


# from bs4 import BeautifulSoup            #网页解析，获取数据
# import re                                #正则表达式，进行文字匹配
# import urllib.request,urllib.error       #制定URL，获取网页数据
#
#
# def main():
#     baseURL="https://movie.douban.com/top250?start="
#     # askURL(baseURL)
#     getData(baseURL)
#
#
# def askURL(url):                #爬取整个网页
#     head={"User-Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89 Safari / 537.36"}
#     request=urllib.request.Request(url,headers=head)
#     response=urllib.request.urlopen(request)
#     html=response.read().decode("utf-8")
#     return html
#
# def getData(baseURL):
#     for i in range(0,10):
#         url=baseURL+str(i*25)
#
#         html=askURL(url)                    #接收函数执行过的爬取的网页
#         print(html)
#
#
# if __name__=="__main__":
#     main()









import re                                   #网页解析，获取数据
from bs4 import BeautifulSoup               #正则表达式，进行文字匹配
import urllib.request,urllib.error          #制定URL，获取网页数据
import xlwt
import sqlite3

findlink=r'<a class="" href="(.*?)"'
findname=r'<span class="title">(.*?)</span>'
def main():
    dbpath="testSpider.db"                             #用于指定数据库存储路径
    savepath="testSpider.xls"                          #用于指定excel存储路径
    baseURL="https://movie.douban.com/top250?start="   #爬取的网页初始链接
    dataList=getData(baseURL)
    saveData(dataList,savepath)
    saveDataDb(dataList,dbpath)
def askURL(url):  #得到指定网页信息的内容 #爬取一个网页的数据
    # 用户代理，本质上是告诉服务器，我们是以什么样的机器来访问网站，以便接受什么样的水平数据
   head={"User-Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89 Safari / 537.36"}
   request=urllib.request.Request(url,headers=head)         #request对象接受封装的信息，通过urllib携带headers访问信息访问url
   response=urllib.request.urlopen(request)                  #用于接收返回的网页信息
   html=response.read().decode("utf-8")                      #通过read方法读取response对象里的网页信息，使用“utf-8”
   return  html                                             #返回捕获的网页内容，此时还是未处理过的
def getData(baseURL):
    dataList=[]                                     #初始化datalist用于存储获取到的数据
    for i in range(0,10):
        url=baseURL+str(i*25)
        html=askURL(url)                                    #保存获取到的源码
        soup=BeautifulSoup(html,"html.parser")              #对html进行逐一解析，使用html.parser解析器进行解析
        for item in soup.find_all("div",class_="item"):     #查找符合要求的字符串 ，形成列表，find_all是查找所有的class是item的div
            data=[]                                         #初始化data，用于捕获一次爬取一个div里面的内容
            item=str(item)                                  #将item数据类型转化为字符串类型
            # print(item)
            link=re.findall(findlink,item)[0]               #使用re里的findall方法根据正则提取item里面的电影链接
            data.append(link)                               #将网页链接追加到data里
            name=re.findall(findname,item)[0]               #使用re里的findall方法根据正则提取item里面的电影名字
            data.append(name)                               #将电影名字链接追加到data里
            # print(link)
            # print(name)
            dataList.append(data)                           #将捕获的电影链接和电影名存到datalist里面
    return dataList                                         #返回一个列表，里面存放的是每个电影的信息
    print(dataList)

def saveData(dataList,savepath):                            #保存捕获的内容到excel里，datalist是捕获的数据列表，savepath是保存路径
    book=xlwt.Workbook(encoding="utf-8",style_compression=0)#初始化book对象，这里首先要导入xlwt的包
    sheet=book.add_sheet("test",cell_overwrite_ok=True)     #创建工作表
    col=["电影详情链接","电影名称"]                           #列名
    for i in range(0,2):
        sheet.write(0,i,col[i])                             #将列名逐一写入到excel
    for i in range(0,250):
        data=dataList[i]                                    #依次将datalist里的数据获取
        for j in range(0,2):
            sheet.write(i+1,j,data[j])                      #将data里面的数据逐一写入
    book.save(savepath)                                     #保存excel文件

def saveDataDb(dataList,dbpath):
    initDb(dbpath)                                          #用一个函数初始化数据库
    conn=sqlite3.connect(dbpath)                            #初始化数据库
    cur=conn.cursor()                                       #获取游标
    for data in dataList:
        for index in range(len(data)):
            data[index]='"'+data[index]+'" '                #将每条数据都加上""
        #每条数据之间用，隔开，定义sql语句的格式
        sql='''
            insert into test(link,name) values (%s)         
        '''%','.join (data)
        cur.execute(sql)                                    #执行sql语句
        conn.commit()                                       #提交数据库操作
    conn.close()
    print("爬取存入数据库成功！")
def initDb(dbpath):
    conn=sqlite3.connect(dbpath)
    cur=conn.cursor()
    sql='''
        create table test(
            id integer primary key  autoincrement,
            link text,
            name varchar 
            
        )
    '''
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
if __name__=="__main__":       #程序执行入口
    main()