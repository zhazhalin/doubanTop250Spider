#-*- coding = utf-8 -*-
#@Time : 2020/7/26 
#@Author:张家林
#@File : spider.py
#@Software:{PyCharm}


from bs4 import BeautifulSoup            #网页解析，获取数据
import re                                #正则表达式，进行文字匹配
import urllib.request,urllib.error       #制定URL，获取网页数据
import xlwt                              #进行EXCEL操作
import sqlite3                           #数据库操作
from urllib.request import urlretrieve
# 1、爬取网页
# 2、解析数据
# 3、保存数据


def main():
    baseurl="https://movie.douban.com/top250?start="
    datalist=getData(baseurl)
    savepath="豆瓣电影.xls"
    savedata(datalist, savepath)
    dbpath="豆瓣top250.db"
    # savedata2db(datalist,dbpath)

#影片详情链接的规则
findLink=re.compile(r'<a href="(.*?)"')    #创建正则表达式对象，表示规则
#影片图片
findSrcLink=re.compile(r'src="(.*?)"',re.S)   #re.S让换行符包含在字符中
#影片名称
findTitle=re.compile(r'<span class="title">(.*?)</span>')
#影片评分
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge=re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq=re.compile(r'<span class="inq">(.*)</span>')
#影片相关内容
findBd=re.compile(r'<p class="">(.*?) </p>',re.S)

# 1、爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,10):
        url=baseurl+str(i*25)
        html=askURL(url)        #保存获取到的源码
        #逐一解析数据
        j=1
        soup=BeautifulSoup(html,"html.parser")               #对html进行逐一解析，使用html.parser解析器进行解析
        for item in soup.find_all("div" ,class_="item"):     #查找符合要求的字符串 ，形成列表，find_all是查找所有的class是item的div
            data=[]
            item=str(item)
            link=re.findall(findLink,item)[0]
            srcLink=re.findall(findSrcLink,item)[0]
            Title=re.findall(findTitle,item)[0]
            rating=re.findall(findRating,item)[0]
            judge=re.findall(findJudge,item)[0]
            inq=re.findall(findInq,item)
            bd=re.findall(findBd,item)[0].replace("<br/>","")
            data.append(link)             #添加链接
            data.append(srcLink)          #添加图片链接
            data.append(Title)            #添加电影名称
            data.append(rating)           #添加评分
            data.append(judge)            #添加评价
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append("")
            # data.append(inq)              #添加影片概况
            data.append(bd)               #添加相关内容
            # print("影片",j)
            # print("影片详情链接：",link)
            # print("影片图片链接：",srcLink)
            # print("影片片名：",Title)
            # print("影片评分：",rating)
            # print("影片评价人数：",judge)
            # print("影片概况：",inq)
            # print("影片相关内容：",bd)
            # print("\n")
            j+=1
            datalist.append(data)    #把处理好的一部电影装载到datalist
            # print(datalist)
    return datalist

#保存网页数据
def savedata(datalist, savepath):
    print("开始爬取")
    book=xlwt.Workbook(encoding="utf-8")
    sheet=book.add_sheet("豆瓣电影")
    col=("电影详情","图片链接","影片名称","评分","评价数","概况","相关信息")
    for i in range(0,7):
        sheet.write(0,i,col[i])    #列名
    for i in range(0,250):
        print("第%d条信息："%(i+1))
        data=datalist[i]
        for j in range(0,7):
            sheet.write(i+1,j,data[j])
    for i in range(0,5):
        data=datalist[i]
        pic_link=data[1]
        print(pic_link)
        savepicture(pic_link,i)   #执行下载图片函数
    book.save(savepath)

# 下载图片
def savepicture(pic_link,i):
        urlretrieve(pic_link,str(i)+'.jpg')
def savedata2db(datalist,dbpath):
    init_db(dbpath)
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'
        sql='''
            insert into movie(info_link,pic_link,name,score,rated,instroduction,info)
             values (%s)
        '''%",".join (data)
        print(sql)
        cursor.execute(sql)
        conn.commit()
    conn.close()
    print("成功")

def init_db(dbpath):
    conn=sqlite3.connect(dbpath)
    c=conn.cursor()
    sql='''
        create table movie (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            name varchar ,
            score numeric ,
            rated numeric ,
            instroduction varchar ,
            info text 
        )
        
    '''
    cursor=c.execute(sql)
    conn.commit()
    conn.close()



#得到指定网页信息的内容
#爬取一个网页的数据
def askURL(url):
    head={  #模拟浏览器头部信息，像网站发出请求
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89 Safari / 537.36"
    }   #用户代理，本质上是告诉服务器，我们是以什么样的机器来访问网站，以便接受什么样的水平数据
    request=urllib.request.Request(url,headers=head)         #request对象接受封装的信息，通过urllib携带headers访问信息访问url
    html=""                                                  #用于接收返回的网页信息
    try:
        response=urllib.request.urlopen(request)            #通过response对象获得整个网页的信息
        html=response.read().decode("utf-8")                #通过read方法读取response对象里的网页信息，使用“utf-8”
        # print(html)
    except urllib.error as e:
        if hasattr(e,"code"):                               #打印捕获的代码
            print(e.code)
        if hasattr(e,"reason"):                             #打印捕获的原因
            print(e.reason)
    return  html




if __name__ == "__main__":
    main()
    print("爬取完毕")