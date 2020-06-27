'''
@Author: your name
@Date: 2020-05-14 17:45:41
'''
# 获取虎牙直播的真实流媒体地址。
# 现在虎牙直播链接需要密钥和时间戳了

import re,os,json,time
import requests
import datetime
import random
import threading
import subprocess
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from mainwindow import Ui_MainWindow

anchor_status = ["1"]
flag = True
live_video = None
# 退出标识
is_exit = False

def get_real_url(room_id):
    try:
        room_url = 'https://m.huya.com/' + str(room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
        response = requests.get(url=room_url, headers=header).text
        liveLineUrl = re.findall(r'liveLineUrl = "([\s\S]*?)";', response)[0]
        if liveLineUrl:
            if 'replay' in liveLineUrl:
                return '直播录像：' + liveLineUrl
            else:
                real_url = ["https:" + re.sub(r'_\d{4}.m3u8', '.m3u8', liveLineUrl), "https:" + liveLineUrl]
        else:
            real_url = '未开播或直播间不存在'
    except:
        real_url = '未开播或直播间不存在'
    return real_url

def prepare(flv_url):
    global live_video
    # 利用ffmpeg进行录屏
    filename = datetime.datetime.today()
    filename = filename.strftime('%Y-%m-%d-%H%M%S')
    # filename = filename.strftime('%Y-%m-%d%H:%M:%S')
    filename = filename + '.mp4'
    print(filename) # 文件名称类似'%Y-%m-%d%H:%M:%S.flv'格式
    # 文件保存的目录，我把文件存在硬盘上面了
    # file_path = "/media/ych/Seagate\ Backup\ Plus\ Drive/zhibo"
    file_path = "E:\\test"
    live_video = subprocess.Popen('ffmpeg -user_agent \
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36" \
        -i {} -acodec copy -bsf:v h264_mp4toannexb -vcodec copy {}'.format('"%s"' % flv_url, os.path.join(file_path,filename)), \
        shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    while True:
        if is_exit:
            return
        #   stdin, stdout, stderr： 分别表示程序标准输入、输出、错误句柄。
        try:
            line = live_video.stdout.readline().decode('utf-8', 'ignore')
            print(line)
        except Exception as e:
            print("读取cmd内容错误：",e)
            return


    # os.system('ffmpeg -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36" -i {} -acodec copy -bsf:v h264_mp4toannexb -vcodec copy {}'.format('"%s"' % flv_url, os.path.join(file_path,filename)))
def get_state(url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
    # 判断是否开播
    global anchor_status # 是否开播的标记
    response = requests.get(url, headers=headers)
    html = response.content.decode()
    anchor_status = re.findall("上次开播(.*?)</span>" , html)
    # 开播返回None，不开播返回列表
    if anchor_status:
        print("尚未开播")
    else:
        print("正在直播")

class change_status(QThread):
    trigger = pyqtSignal(str)
 
    def __init__(self,url):
        super(change_status, self).__init__()
        self.url = url
        print(url," 构造函数：")
 
    def run(self):
        # 判断是否开播的线程
        print("------change------",is_exit)
        while True:
            if is_exit :
                return
            try:
                get_state(self.url)
                # 随机对直播间进行访问，为防止爬虫被封
                time.sleep(random.randint(10,30))
            except:
                # 如果ip被封或报错，休息60s后继续访问
                time.sleep(60)

class recording(QThread):
    trigger = pyqtSignal(str)
 
    def __init__(self,flv_url):
        super(recording, self).__init__()
        self.flv_url = flv_url

    def run(self):
        global flag,anchor_status
        # 进行录屏的线程
        while True:
            if is_exit :
                return
            print("-------recoding-------")
            print(len(anchor_status) == 0)
            print(flag)
            time.sleep(5)
            if len(anchor_status) == 0 and flag:
                print("---get into self prepare")
                # 进行录屏
                prepare(self.flv_url)
                flag = False
            elif len(anchor_status) != 0:
                flag = True

class endRecord(QThread):
    trigger = pyqtSignal(str)
 
    def __init__(self):
        super(endRecord, self).__init__()

    def run(self):

        global live_video, is_exit
        is_exit = True
        live_video.stdin.write('q'.encode("GBK"))
        live_video.communicate()
        print("结束 捕获")
# UI类
class mywindow(QMainWindow, Ui_MainWindow):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
    # 开始捕获
    def start_bt(self):
        global is_exit,flag
        is_exit = False
        flag = True
        rid = self.lineEdit.text()
        self.label.setText( "房间号：" + rid.strip() )

        real_url = get_real_url(rid) # 房间源地址
        real_url = real_url[0]

        self.change = change_status('https://m.huya.com/' + str(rid))
        self.change.start()

        self.ffm = recording( real_url )
        self.ffm.start()

        # change = threading.Thread(target=change_status,args=('https://m.huya.com/' + str(rid),))
        # ffm = threading.Thread(target=recording,args=(real_url,))
        # change.daemon = True
        # ffm.daemon = True
        # # 开始运行程序
        # change.start()
        # ffm.start()
    # 结束捕获
    def end_bt(self):

        self.thread1 = endRecord()
        self.thread1.start()

    def exit_bt(self):
        print(is_exit,"  is_exit")

    # def print_in_textEdit(self, msg):
    #     self.label.setText(msg)
    #     self.thread_1.exit()


if __name__ == '__main__':
    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    #QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    w = mywindow()
    # 按钮事件
    w.start_Button.clicked.connect(w.start_bt)
    w.end_Button.clicked.connect(w.end_bt)
    w.pushButton_3.clicked.connect(w.exit_bt)

    #设置窗口的标题
    w.setWindowTitle('虎牙hls数据捕捉1.0')
    #显示在屏幕上
    w.show()
    #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())

#     rid = '11342412' # 房间号
