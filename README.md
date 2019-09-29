# 介绍
- 以后关于爬虫的学习内容


##  网易云音乐
- BaseMusic163.py 直接可以运行单线程和多线程
- python3版本，把相关依赖安装即可
- Gevents直接运行，是用协程的方式进行抓取并下载

## Ysts8 音频爬虫
- ysx8-1.py 是优化版本，把核心代码剥离出来，多线程下载，用的selenium headless获取下载地址
- chrome version is 77.0.3865.90
- chromedriver version is 77.0.3865.40
- Ysts8.py 是用的tkinter可视化页面，暂时已经失效，后续待修复