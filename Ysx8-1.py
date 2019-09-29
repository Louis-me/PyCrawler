# -*- coding=utf-8 -*-
import traceback

from fake_useragent import UserAgent

__author__ = 'shikun'
__CreateAt__ = '2019/9/29-11:48'

from bs4 import BeautifulSoup
import re
import urllib.request
import requests
import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
from Threads import BaseThread

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Ysts8():

    def get_play_url(self, url):
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 ' \
                     'Safari/537.36 '
        headers = {'User-Agent': user_agent}
        data = requests.get(url, headers)
        data.encoding = 'gb18030'
        soup = BeautifulSoup(data.text, 'lxml')
        temp = []
        for i in soup.find("div", {"class", "ny_l"}).find_all("li"):
            pattern = re.compile('<a href=(.*?) title=(.*?)">(.*?)</a>', re.S)
            items = re.findall(pattern, str(i))
            if len(items) > 0:
                temp.append([items[0][0], items[0][1], items[0][2]])
        return temp

    def get_audio_url(self, paly_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--allow-insecure-localhost")
        driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)
        audio_list = []
        urls = paly_url
        for url in urls:
            print("https://www.ysx8.net" + url[0][1:len(url[0]) - 1])
            print('请求开始...')
            driver.get("https://www.ysx8.net" + url[0][1:len(url[0]) - 1])
            print('请求中...')
            time.sleep(0.5)
            try:
                frame = driver.find_element_by_xpath('//*[@id="play"]')
                driver.switch_to.frame(frame)
                select = driver.find_element_by_id("jp_audio_0")
                WebDriverWait(driver, 20).until(lambda x: EC.presence_of_element_located(select))
                audio = select.get_attribute('src')
                if audio:
                    audio_list.append({"url": audio, "name": url[1][1:]})
            except:
                driver.quit()
        print(audio_list)
        driver.quit()
        return audio_list

    def download(self, data):
        print(unquote(data["url"]))
        if os.path.isfile(PATH("mp3/" + data["name"])):
            print("%s已经被下载了" % data["name"])
        else:
            urllib.request.urlretrieve(data["url"], '%s' % unquote(PATH("mp3/" + data["name"])))
            print("%s下载成功" % data["name"])


def multi_thread():
    url = "https://www.ysx8.net/Yshtml/Ys14863.html"
    start_time = time.time()
    threads = []
    ys = Ysts8()

    paly_url = ys.get_play_url(url)
    audio_url = ys.get_audio_url(paly_url)
    count = len(audio_url)
    for i in range(0, count):
        threads.append(BaseThread(ys.download(audio_url[i])))
    for j in range(0, count):
        threads[j].start()
    for k in range(0, count):
        threads[k].join()
    end_time = time.time()
    print("共耗时%.2f" % (end_time - start_time) + "秒")


if __name__ == "__main__":
    multi_thread()
