from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HuYaList(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, url):
        super(HuYaList, self).__init__()
        self.url = url
        print("当前url值：", self.url)

    def run(self):
        # url = "https://www.huya.com/880243"
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

        self.driver.set_window_size(1280, 960)
        self.driver.get(self.url)
        self.awaitClass("playbill-box")
        playbox = self.driver.find_element_by_class_name("playbill-box")
        lists = playbox.find_elements_by_tag_name("li")
        datas = []
        for v in lists:
            # print(v)
            # print(v.get_attribute('data-id'),v.get_attribute('data-anchor'),v.get_attribute('data-yy'),v.get_attribute('data-room'))
            obj = {}
            obj['dataanchor'] = v.get_attribute('data-anchor')
            obj['dataid'] = v.get_attribute('data-id')
            obj['datayy'] = v.get_attribute('data-yy')
            obj['roomid'] = self.mendStr(v.get_attribute('data-room'))
            obj['playtime'] = self.mendStr(v.find_element_by_class_name("item-time").get_attribute('textContent'))
            obj['playname'] = self.mendStr(v.find_element_by_class_name("msg-nick").get_attribute('textContent'))
            obj['playimg'] = v.find_element_by_class_name("anchor-img").get_attribute('src')
            # print(obj)
            datas.append(obj)
        print(type(datas))
        self.trigger.emit(datas)
        # return datas

    def mendStr(self, _str):
        if len(_str) > 15:
            return _str
        for i in range(15 - len(_str)):
            _str = _str + " "
        return _str
        # 等待对应元素加载完毕

    def awaitClass(self, _name):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, _name))
            )
        except Exception as e:
            print("没有等待到元素", e)
