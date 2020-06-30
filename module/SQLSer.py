#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SQLSer.py    
@Contact :   80491636@qq.com
@Modify Time :   2020/6/29 17:39 
--------------------------------------
'''
import time

import pymysql


class SqlSer(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='huya',
            charset='utf8',
        )

        # 获取游标
        self.cursor = self.connect.cursor()

    def addData(self,datas,filename):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 插入数据
        sql = "INSERT INTO hyvideo (data_id, data_room, playtime, playname, img, filename, date) VALUES \
        ( '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        data = (datas['dataid'], datas['roomid'], datas['playtime'], datas['playname'], datas['playimg'], filename, t)
        self.cursor.execute(sql % data)
        self.connect.commit()
        print('成功插入', self.cursor.rowcount, '条数据')


    def closeSer(self):
        # 关闭连接
        self.cursor.close()
        self.connect.close()

 
