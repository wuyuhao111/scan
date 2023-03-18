import threading

import gevent
from gevent import monkey

monkey.patch_all()
import requests
import json, hashlib
from gevent.queue import Queue

url_line = []
success = []

class gwhatweb(object):
    def __init__(self, url):
        self.tasks = Queue()  # Queve是队列，self.tasks.put(i)就是把数据填充到队列里
        self.url = url.rstrip("/")  # url分割
        fp = open('E:/github/scan/dictionary/data.json', 'r', encoding="utf-8")  # 打开字典文件
        webdata = json.load(fp)
        for i in webdata:
            self.tasks.put(i)  # 处理字典
        fp.close()
        print("webdata total:%d" % len(webdata))

    def _GetMd5(self, body):  # 将 网页body部分先utf-8编码，在计算MD5（用来识别图标，比对MD5）
        m2 = hashlib.md5()
        m2.update(body.encode("utf8"))
        return m2.hexdigest()

    def _clearQueue(self):  # 清除一个线程
        while not self.tasks.empty():
            self.tasks.get()

    def _worker(self):  # 任务处理
        data = self.tasks.get()  # 取出队列元素
        test_url = self.url + data["url"]  # 获取url
        try:
            r = requests.get(test_url, timeout=10)  # timeout表示处理10秒，如果10秒还没请求到，就不请求了
            if (r.status_code != 200):  # 判断响应码
                return
            rtext = r.text  # 复制网页文本信息
            if rtext is None:
                return
        except:
            rtext = ''

        if data["re"]:  # 判断是否需要正则匹配（字典里如果是图片文件路径，也可以比对对他的MD5值）
            if (rtext.find(data["re"]) != -1):
                result = data["name"]  # 取出字典里CMS名称
                CMS = "CMS:"+ result + " Judge:"+ test_url + " re:" + data["re"]
                success.append(CMS)
                print("CMS:%s Judge:%s re:%s" % (result, test_url, data["re"]))
                self._clearQueue()  # 清除队列
                return True
        else:
            md5 = self._GetMd5(rtext)  # 用来比对MD5值
            if (md5 == data["md5"]):
                result = data["name"]  # 取出字典里CMS名称
                CMS = "CMS:" + result + " Judge:" + test_url + " re:" + data["md5"]
                success.append(CMS)
                print("CMS:%s Judge:%s md5:%s" % (result, test_url, data["md5"]))
                self._clearQueue()  # 清除队列
                return True

    def _boss(self):
        while not self.tasks.empty():
            self._worker()

    def whatweb(self, maxsize=100):
        allr = [gevent.spawn(self._boss) for i in range(maxsize)]  # 变成列表存储
        gevent.joinall(allr)  # 加载列表


def cms(url):
    print("正在进行CMS识别")
    if "http://" not in url:
        url = "http://" + url
    g = gwhatweb(url)
    g.whatweb(1000)


def read():
    for urls in open('E:/github/scan/dictionary/ip.txt'):
        urls = urls.replace("\n", "")
        url_line.append(urls)


def cms_r():
    for urls_urls in url_line:
        g = gwhatweb(urls_urls)
        g.whatweb(1000)


def write(f):
    try:
        for cms in success:
            f.write(cms + "\n")
    except Exception as e:
        print(e)
        pass


def thread_cms():
    try:
        with open('E:/github/scan/result/cms_result.txt', mode='w', encoding='utf-8') as f:
            threads = []
            t1 = threading.Thread(target=read)
            threads.append(t1)
            t2 = threading.Thread(target=cms_r)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
            threads.append(t2)
            t3 = threading.Thread(target=write, args=(f,))
            threads.append(t3)
            for t in threads:  # 遍历线程列表
                t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
                t.start()
                t.join()
            f.close()
    except Exception as e:
        print(e)
        pass
