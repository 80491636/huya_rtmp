from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time



url = "https://www.huya.com/880243"
driver = webdriver.Chrome(executable_path = "chromedriver.exe")	

# 等待对应元素加载完毕
def awaitClass(_name):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, _name))
        )
    except Exception as e:
        print("没有等待到元素",e)

driver.set_window_size(1280,960)
driver.get(url)		
awaitClass("playbill-box")
playbox = driver.find_element_by_class_name("playbill-box")
lists = playbox.find_elements_by_tag_name("li")
for v in lists:
    # print(v)
    # print(v.get_attribute('data-id'),v.get_attribute('data-anchor'),v.get_attribute('data-yy'),v.get_attribute('data-room'))
    roomid = v.get_attribute('data-room')
    playtime = v.find_element_by_class_name("item-time").get_attribute('textContent')
    playname = v.find_element_by_class_name("msg-nick").get_attribute('textContent')
    playimg = v.find_element_by_class_name("anchor-img").get_attribute('src')
    print(roomid,playtime,playname,playimg)

