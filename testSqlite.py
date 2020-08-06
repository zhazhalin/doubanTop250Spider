#-*- coding = utf-8 -*-
#@Time : 2020/7/27 
#@Author:张家林
#@File : testSqlite.py
#@Software:{PyCharm}

import sqlite3
# conn=sqlite3.connect("test.db")
# print("opened database sucessfully")


# conn=sqlite3.connect("test.db")
# print("opened database sucessfully")
# c=conn.cursor()          #获取游标
# sql='''
#     create table company(
#         id int  primary key autoincement not null,
#         name text not null ,
#         age int not null ,
#         address char(50) ,
#         salary int not null
#     );
# '''
# c.execute(sql)          #执行sql语句
# conn.commit()           #提交数据库操作
# conn.close()            #关闭数据库操作
#
# print("成功建表")


# conn=sqlite3.connect("test.db")
# c=conn.cursor()     #获取游标
# print("opened database sucessfully")
# sql='''
#     insert into company (id,name,age,address,salary)
#     values (1,"渣渣林",20,"温县",200000)
# '''
# c.execute(sql)          #执行sql语句
# conn.commit()           #提交数据库操作
# conn.close()            #关闭数据库












# #插入数据
# conn=sqlite3.connect("test.db")
# c=conn.cursor()
# sql='''
#     insert into company (id,name,age,address,salary)
#     values (
#         2,"渣渣林",20,"温县",20000
#     )
# '''
# c.execute(sql)
# conn.commit()
# conn.close()
# print("插入成功")

conn=sqlite3.connect("test.db")      #连接数据库
c=conn.cursor()
sql="select * from company"
cursor=c.execute(sql)
for row in cursor :
    print("id=",row[0])
    print("name=",row[1])
    print("age=",row[2])
    print("adress=",row[3])
    print("salary=",row[4],"\n")
conn.close()