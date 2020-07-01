#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AutoTimer.py    
@Contact :   80491636@qq.com
@Modify Time :   2020/7/1 11:24 
--------------------------------------
'''
import time

from PyQt5.QtCore import QThread, pyqtSignal


class AutoTimer(QThread):
    trigger = pyqtSignal(str)

    def __init__(self,datas,startcall,endcall):
        super(AutoTimer, self).__init__()
        self.datas = datas
        self.runis = False
        self.startcall = startcall
        self.endcall = endcall

    def run(self):

        while True:

            localtime = time.localtime(time.time())
            tm_hour = localtime.tm_hour
            tm_min = localtime.tm_min
            tm_sec = localtime.tm_sec
            tm_year = time.strftime("%Y-%m-%d", time.localtime())
            start = tm_year + " 17:55:00"
            end = tm_year + " 01:55:00"
            startTime = time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))
            endTime = time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))
            # if startTime
            # 开始捕获时间
            if tm_sec == 30 or tm_sec == 0:
                if self.runis == False:
                    self.startcall()
                    self.runis = True
            # 结束捕获时间
            if tm_sec == 50 or tm_sec == 20:
                if self.runis :
                    # 调用结束捕获
                    self.endcall()
                    self.runis = False

            print("本地时间为 :", localtime)
            print("时：",localtime.tm_hour," 分：",localtime.tm_min," 秒：",localtime.tm_sec)
            time.sleep(2)
        # self.trigger.emit("a")

