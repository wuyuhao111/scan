import threading

import requests, sys
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 设置好开始时间点
strat = time.time()

success = []
ip_line = []

lock = threading.Lock()


class G:
    rb1 = None
    rb2 = None
    rb3 = None


def chax(url):
    lid = url
    # 设置浏览器头过反爬
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # 设置好url
    url = "http://site.ip138.com/{}/".format(lid)
    urldomain = "http://site.ip138.com/{}/domain.htm".format(lid)
    url2 = "http://site.ip138.com/{}/beian.htm".format(lid)
    url3 = "http://site.ip138.com/{}/whois.htm".format(lid)
    # 打开网页
    rb = requests.get(url, headers=head)
    G.rb1 = requests.get(urldomain, headers=head)
    G.rb2 = requests.get(url2, headers=head)
    G.rb3 = requests.get(url3, headers=head)
    # 获取内容并用html的方式返回
    gf = BeautifulSoup(rb.content, 'html.parser')
    print('[+]IP解析记录')
    # 读取内容里的p标签
    for x in gf.find_all('p'):
        # 使用text的内容返回
        link = x.get_text()
        success.append(url + " :" + "ip解析记录:" + link + "\n")
        print(link)


def cms_cms(url):  # 单个ip使用
    print("正在进行whois查询")
    chax(url)
    gf1 = BeautifulSoup(G.rb1.content, 'html.parser')
    print('[+]子域名查询')
    for v in gf1.find_all('p'):
        link2 = v.get_text()
        success.append("子域名查询：" + link2 + "\n")
        print(link2)
    gf2 = BeautifulSoup(G.rb2.content, 'html.parser')
    print('[+]备案查询')
    for s in gf2.find_all('p'):
        link3 = s.get_text()
        success.append("备案信息：" + link3 + "\n")
        print(link3)
    gf3 = BeautifulSoup(G.rb3.content, 'html.parser')
    print('[+]whois查询')
    for k in gf3.find_all('p'):
        link4 = k.get_text()
        success.append("whois信息：" + link4 + "\n")
        success.append("------------------------------------------------")
        print(link4)
    end = time.time()
    print('查询耗时:', end - strat)


def cms_cms_r(url):  # 批量使用
    print("正在进行whois查询")
    chax(url)
    gf1 = BeautifulSoup(G.rb1.content, 'html.parser')
    print('[+]子域名查询')
    for v in gf1.find_all('p'):
        link2 = v.get_text()
        success.append(url + " :" + "子域名查询：" + link2 + "\n")
        print(link2)
    gf2 = BeautifulSoup(G.rb2.content, 'html.parser')
    print('[+]备案查询')
    for s in gf2.find_all('p'):
        link3 = s.get_text()
        success.append(url + " :" + "备案信息：" + link3 + "\n")
        print(link3)
    gf3 = BeautifulSoup(G.rb3.content, 'html.parser')
    print('[+]whois查询')
    for k in gf3.find_all('p'):
        link4 = k.get_text()
        success.append(url + " :" + "whois信息：" + link4 + "\n")
        print(link4)
    end = time.time()
    print('查询耗时:', end - strat)


def write():
    lock.acquire()
    try:
        with open('E:/github/scan/result/whois_result.txt', mode='w', encoding='utf-8') as f:
            for url in success:
                f.write(url)
    except Exception as e:
        print(e)
        pass
    f.close()
    lock.release()


def information():
    try:
        urls = open('E:/github/scan/dictionary/ip.txt')
        with ThreadPoolExecutor(max_workers=5) as executor:
            for url in urls:
                try:
                    executor.submit(cms_cms_r, url.strip())
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass


def thread():
    print("正在进行whois查询\n")
    try:
        threads = []
        t1 = threading.Thread(target=information)
        threads.append(t1)
        t2 = threading.Thread(target=write)
        threads.append(t2)
        for t in threads:  # 遍历线程列表
            t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print(e)
        pass


