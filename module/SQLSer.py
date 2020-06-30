#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SQLSer.py    
@Contact :   80491636@qq.com
@Modify Time :   2020/6/29 17:39 
--------------------------------------
'''

import pymysql


class Class(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3310,
            user='root',
            passwd='123456',
            db='huya',
            charset='utf8'
        )

        # 获取游标
        self.cursor = self.connect.cursor()

    def addData(self,datas):
        for v in datas:
            # 插入数据
            sql = "INSERT INTO hyvideo (data_id, data_room, playtime, playname, img, filename, musicname, uploadis, date) VALUES \
            ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )"
            data = (v['dataid'], v['roomid'], v['playtime'], v['playname'], v['playimg'],)
            self.cursor.execute(sql % data)
            self.connect.commit()
            print('成功插入', self.cursor.rowcount, '条数据')


    def closeSer(self):
        # 关闭连接
        self.cursor.close()
        self.connect.close()

 
