import time
from multiprocessing import Process
from gevent import monkey
import urllib.request
import BaseMusic163
monkey.patch_all()
import gevent
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
'''
协程发请求,
经过测试，居然只要6秒左右
'''


class Producer(object):
    def __init__(self):
        self._rungevent()

    def _rungevent(self):
        jobs = []
        id = "2786226719"  # 播放的列表id
        start_time = time.time()
        mc = BaseMusic163.Music163()
        data = mc.get_music_163(id)
        count = len(data)
        for i in range(count):  # windows下有1024端口限制
            jobs.append(gevent.spawn(self.produce(data[i])))
        gevent.joinall(jobs)
        end_time = time.time()
        print("共耗时%.2f" % (end_time - start_time) + "秒")

    def produce(self, value):
        if os.path.isfile(PATH("mp3/" + value[1] + ".mp3")):
            print("%s已经被下载了" % value[1])
        else:
            url = 'http://music.163.com/song/media/outer/url?id=' + value[0] + '.mp3'
            urllib.request.urlretrieve(url, '%s' % PATH("mp3/" + value[1] + ".mp3"))
            print("%s下载成功" % value[1])


def main():
    p1 = Process(target=Producer, args=())
    p1.start()


if __name__ == '__main__':
    main()
