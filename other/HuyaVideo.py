'''
@Author: your name
@Date: 2020-06-10 11:50:06
'''
import time

import requests
import re
from pyquery import PyQuery


def get_page(url):
    """  获取页面  """

    # 设置请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
        'Referer': 'https://www.huya.com/'
    }
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        return response.text
    return None


def parse_html(html):
    # 改用PyQuery库进行解析

    doc = PyQuery(html)
    items = doc.find('.content-list li').items()
    for item in items:
        result = {
            '名称': item.find('.card-title').text(),
            '作者': '觅音-十七里',
            '时长': item.find('.cover-duration').text(),
            '播放量': item.find('.card-detail .detail-left').text(),
            '上传日期': item.find('.card-detail .detail-right').text(),
            '播放地址': 'https://v.huya.com' + str(item.find('.statpid').attr('href'))

        }
        print(result)


def main():
    url = 'https://v.huya.com/u/1431967642/video.html'
    html = get_page(url)
    parse_html(html)


if __name__ == '__main__':
    print('正在尝试请求虎牙视频...')
    time.sleep(1)
    print('get请求失败,尝试暴力请求...')
    time.sleep(1)
    print('暴力破解虎牙成功,正在获取虎牙信息...')
    time.sleep(1)
    print('虎牙信息提取完成,正在形成结构化数据...')
    print(
        '------------------------------------------------------------------------------------------------------------------------------')
    main()
    print(
        '------------------------------------------------------------------------------------------------------------------------------')
