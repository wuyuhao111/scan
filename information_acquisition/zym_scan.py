import random
import threading
from concurrent.futures import ThreadPoolExecutor
import HackRequests

urls_line = []
urls_line_r = []
success = []
file_line = []

lock = threading.Lock()


def Hackreq(url):
    hack = HackRequests.hackRequests()
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # header['User-Agent'] = random.choice(agents)
    try:
        uu = hack.http(url, retries=3)
        if uu.status_code == 200:
            print(r"[+] " + url)
            success.append(url + "\n")  # 成功访问的放一个集合
        else:
            print(r"[-] " + url)
    except:
        pass


def openFile_r():  # 这里做一个进程放链接
    for urls in urls_line:
        if "http://" in urls:
            urls = urls.replace("http://", "")
        if "https://" in urls:
            urls = urls.replace("https://", "")
        if "www." in urls:
            urls = urls.replace("www.", "")
        for file in file_line:
            url = file + urls
            if "http://" not in url:
                url = "http://" + url
            urls_line_r.append(url)  # 去掉\n


def openFile(urls):  # 这里做一个进程放链接
    if "http://" in urls:
        urls = urls.replace("http://", "")
    if "https://" in urls:
        urls = urls.replace("https://", "")
    if "www." in urls:
        urls = urls.replace("www.", "")
    for file in file_line:
        url = file + urls
        if "http://" not in url:
            url = "http://" + url
        urls_line_r.append(url)  # 去掉\n


def write():
    lock.acquire()
    try:
        with open('E:/github/scan/result/nmap_result.txt', mode='w', encoding='utf-8') as f:
            for url in success:
                f.write(url)
    except Exception as e:
        print(e)
        pass
    f.close()
    lock.release()


def read_zym():
    try:
        for file in open('E:/github/scan/dictionary/zym.txt', 'r', encoding="utf-8"):
            file = file + "."
            file = file.replace('\n', '')
            file_line.append(file)
    except Exception as e:
        print(e)
        pass


def read_url():
    try:
        for url in open('E:/github/scan/dictionary/url.txt', 'r', encoding="utf-8"):
            url = url.replace("\n", "")
            urls_line.append(url)
    except Exception as e:
        print(e)
        pass


def thread_r():
    print("正在进行子域名查询")
    threads = []
    try:
        t1 = threading.Thread(target=read_zym)
        threads.append(t1)
        t2 = threading.Thread(target=read_url)
        threads.append(t2)
        t3 = threading.Thread(target=openFile_r)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
        threads.append(t3)
        t4 = threading.Thread(target=information)
        threads.append(t4)
        t5 = threading.Thread(target=write)
        threads.append(t5)
        try:
            for t in threads:  # 遍历线程列表
                t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
                t.start()
            for t in threads:
                t.join()
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass


def thread(url):
    print("正在进行子域名查询")
    threads = []
    try:
        t1 = threading.Thread(target=read_zym)
        threads.append(t1)
        t2 = threading.Thread(target=openFile, args=(url,))  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
        threads.append(t2)
        t3 = threading.Thread(target=information)
        threads.append(t3)
        t4 = threading.Thread(target=write)
        threads.append(t4)
        try:
            for t in threads:  # 遍历线程列表
                t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
                t.start()
            for t in threads:
                t.join()
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass


def information():
    try:
        urls = urls_line_r
        with ThreadPoolExecutor(max_workers=10) as executor:
            for url in urls:
                try:
                    executor.submit(Hackreq, url.strip())
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    thread_r()
    # thread("baidu.com")
