import datetime, os, random, re, subprocess, time
import requests
from PyQt5.QtCore import QThread, pyqtSignal

anchor_status = []  # 是否开播的标记
live_video = None  # subprocess.Popen 返回对象
is_exit = False  # 退出标识


def get_real_url(room_id):
    """
    获取房间直播状态
    @param room_id: 房间号
    @return:开播状态
    """
    global is_exit
    is_exit = False
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


class change_status(QThread):


    def __init__(self, url):
        super(change_status, self).__init__()
        self.url = url

    def run(self):
        global is_exit
        # 判断是否开播的线程
        print("------change------", is_exit)
        while True:
            print("change_status")
            if is_exit:
                return
            try:
                get_state(self.url)
                # 随机对直播间进行访问，为防止爬虫被封
                time.sleep(random.randint(10, 30))
            except:
                # 如果ip被封或报错，休息60s后继续访问
                time.sleep(60)


def prepare(flv_url, file_path):
    global live_video, is_exit
    # 利用ffmpeg进行录屏
    filename = datetime.datetime.today()
    filename = filename.strftime('%Y-%m-%d-%H%M%S')
    filename = filename + '.mp4'
    print(os.path.join(file_path, filename))  # 文件名称类似'%Y-%m-%d%H:%M:%S.flv'格式
    live_video = subprocess.Popen(
        'ffmpeg -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36" -i {} -acodec copy -bsf:v h264_mp4toannexb -vcodec copy {}'.format(
            '"%s"' % flv_url, os.path.join(file_path, filename)), shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    # os.system('ffmpeg -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36" -i {} -acodec copy -bsf:v h264_mp4toannexb -vcodec copy {}'.format('"%s"' % flv_url, os.path.join(file_path,filename)))
    while True:
        if is_exit:
            return
        #   stdin, stdout, stderr： 分别表示程序标准输入、输出、错误句柄。
        try:
            line = live_video.stdout.readline().decode('utf-8', 'ignore')
            # print(line)
        except Exception as e:
            print("读取cmd内容错误：", e)
            return


def get_state(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
    # 判断是否开播
    global anchor_status  # 是否开播的标记
    response = requests.get(url, headers=headers)
    html = response.content.decode()
    anchor_status = re.findall("上次开播(.*?)</span>", html)
    print("anchor_status", anchor_status)
    # 开播返回None，不开播返回列表
    if anchor_status:
        print("尚未开播")
    else:
        print("正在直播")


class recording(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, flv_url, file_path):
        super(recording, self).__init__()
        self.flv_url = flv_url
        self.file_path = file_path

    def run(self):
        global anchor_status, is_exit
        # 进行录屏的线程
        while True:
            if is_exit:
                return
            print("-------recoding-------")
            print(len(anchor_status) == 0)
            time.sleep(5)
            if len(anchor_status) == 0:
                print("---get into self prepare")
                # 进行录屏
                prepare(self.flv_url, self.file_path)


# 结束捕获视频流
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
