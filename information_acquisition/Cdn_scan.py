import os
from concurrent.futures import ThreadPoolExecutor

success = []

def cdn(urls):
    print("\n正在进行cdn查询，请输入正确格式\n")
    try:
        if "www" in urls:
            if "http://" not in urls:
                url = urls.replace('www', 'http://www')
                ns = "nslookup " + url
                data = os.popen(ns, "r").read()
                if data.count(".") > 8:
                    print("[-]"+url+" 存在CDN")
                else:
                    print("[+]"+url+" 不存在CDN")
    except Exception as e:
        print(e)
        pass


def cdn_r():
    try:
        urls = open('E:/github/scan/dictionary/ip.txt')
        with ThreadPoolExecutor(max_workers=2) as executor:
            for url in urls:
                try:
                    executor.submit(cdn, url.strip())
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass
