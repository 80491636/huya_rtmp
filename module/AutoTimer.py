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

    def __init__(self,startcall,endcall):
        super(AutoTimer, self).__init__()
        self.runis = False
        self.startcall = startcall
        self.endcall = endcall

    def run(self):

        while True:
            # 将格式字符串转换为时间戳
            localtime = time.localtime(time.time())
            ticks = time.time()
            tm_year = time.strftime("%Y-%m-%d", localtime)
            start = tm_year + " 17:55:00"
            end = tm_year + " 01:55:00"
            startTime = time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))
            endTime = time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))
            print(ticks,startTime,endTime)
            if ticks < startTime and ticks > endTime:
                return
            tm_hour = localtime.tm_hour
            tm_min = localtime.tm_min
            # tm_sec = localtime.tm_sec
            # 开始捕获时间
            if tm_min == 30 or tm_min == 0:
                if self.runis == False:
                    self.startcall()
                    self.runis = True
            # 结束捕获时间
            if tm_min == 50 or tm_min == 20:
                if self.runis :
                    # 调用结束捕获
                    self.endcall()
                    self.runis = False
                    self.trigger.emit("quit")
            time.sleep(10)
        # self.trigger.emit("a")

