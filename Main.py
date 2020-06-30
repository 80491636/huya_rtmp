'''
@Author: your name
@Date: 2020-05-14 17:45:41
'''
# 获取虎牙直播的真实流媒体地址。
# 现在虎牙直播链接需要密钥和时间戳了

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow
from module.FfmThread import get_real_url, change_status, recording, endRecord

from module.HuYaList import HuYaList


# UI类
class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    # 开始捕获
    def start_bt(self):

        rid = self.roomlineE.text()
        # self.label.setText("房间号：" + rid.strip())
        real_url = get_real_url(rid.strip())  # 房间源地址
        real_url = real_url[0]
        print(rid.strip(), real_url)
        self.change = change_status('https://m.huya.com/' + str(rid))
        self.change.start()
        # 这个线程没有结束
        self.ffm = recording(real_url, self.path_lineE.text())
        self.ffm.start()

    def end_bt(self):

        self.thread1 = endRecord()
        self.thread1.start()

    """
    获取直播列表
    """

    def list_bt(self):

        print("点击按钮 视频列表")
        self.huyalist = HuYaList("https://www.huya.com/880243")
        self.huyalist.start()
        self.huyalist.trigger.connect(self.UpText)

    """
    直播列表回调
    @list datas:  主播预告列表
    """

    def UpText(self, datas):
        i = 0
        test = 0  # 当前正在直播的位置
        for v in datas:
            playtime = v['playtime']
            if playtime.find("直播") >= 0:
                test = i
            self.listWidget.addItem(v['roomid'] + v['playtime'] + v['playname'])
            i = i + 1
        self.listWidget.setCurrentRow(test)
        self.roomlineE.setText(datas[test]['roomid'])
        self.path_lineE.setText("H:\\test")
        self.label_2.setText("直播列表获取成功，一切准备就绪。")

    def pre_bt(self):

        test = self.listWidget.currentRow()
        if test > 0:
            test = test - 1
            self.listWidget.setCurrentRow(test)
            _str = self.listWidget.item(test).text()
            t = _str.split(" ")
            self.roomlineE.setText(t[0])
        else:
            self.label_2.setText("已经是第一条了。")

    def next_bt(self):

        test = self.listWidget.currentRow()
        print(self.listWidget.count())
        if test < self.listWidget.count() - 1:
            test = test + 1
            self.listWidget.setCurrentRow(test)
            _str = self.listWidget.item(test).text()
            t = _str.split(" ")
            self.roomlineE.setText(t[0])
        else:
            self.label_2.setText("已经是最后一条了。")


if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    w = mywindow()
    # 按钮事件
    w.list_Button.clicked.connect(w.list_bt)
    w.start_Button.clicked.connect(w.start_bt)
    w.end_Button.clicked.connect(w.end_bt)
    w.pre_Button.clicked.connect(w.pre_bt)
    w.next_Button.clicked.connect(w.next_bt)
    # 设置窗口的标题
    w.setWindowTitle('虎牙hls数据捕捉1.0')
    # 显示在屏幕上
    w.show()
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
