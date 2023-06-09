import random
import threading

import HackRequests

urls_line = []
urls_line_r = []
success = []
file_line = []


def Hackreq():
    hack = HackRequests.hackRequests()
    agents = [
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）",
        "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider-cpro; +http://www.baidu.com/search/spider.html)"
    ]
    header = {
        "Host": "guit.edu.cn",
        "Content-Type": "application / json",
        "Connection": "close",
        "Accept": "*/*",
        "Accept-Language": "zh-CN",
        "Accept-Encoding": "gzip, deflate"
    }
    header['User-Agent'] = random.choice(agents)
    for url in urls_line:
        try:
            uu = hack.http(url, retries=3)
            if uu.status_code == 200:
                print(r"[+] " + url)
                success.append(url + "\n")  # 成功访问的放一个集合
            else:
                print(r"[-] " + url)
        except:
            pass


def openFile(urls):  # 这里做一个进程放链接
    if file_line != 0:
        for file in file_line:
            url = urls + file
            if "http://" not in url:
                url = "http://" + url
            urls_line.append(url)  # 去掉\n
    else:
        exit(0)


def write(f):  # 将成功访问的起一个线程写入文件
    try:
        for url in success:
            f.write(url)
    except Exception as e:
        print(e)
        pass


def file_file():
    try:
        for file in open('E:/github/scan/dictionary/file.txt', 'r', encoding="utf-8"):
            if '/' not in file:
                file = r'/' + file
            file = file.replace('\n', '')
            file_line.append(file)
    except Exception as e:
        print("file.txt不存在")
        pass

def thread(url_url):
    print("正在进行文件路径爆破\n")
    try:
        with open('E:/github/scan/result/file_scan_result.txt', mode='w', encoding='utf-8') as f:
            threads = []
            t1 = threading.Thread(target=file_file)
            threads.append(t1)
            t2 = threading.Thread(target=openFile, args=(url_url,))  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
            threads.append(t2)
            t3 = threading.Thread(target=Hackreq)
            threads.append(t3)
            t4 = threading.Thread(target=write, args=(f,))
            threads.append(t4)
            for t in threads:  # 遍历线程列表
                t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
                t.start()
            for t in threads:
                t.join()
            f.close()
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    thread("127.0.0.1")