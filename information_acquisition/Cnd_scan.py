import os

def cdn(urls):
    print("\n正在进行cdn查询，请输入正确格式\n")
    global url, data
    if "www" in urls:
        if "http://" not in urls:
            url = urls.replace('www', 'http://www')
        ns = "nslookup " + url
        data = os.popen(ns, "r").read()
    if data.count(".") > 8:
        print("[-]"+url+" 存在CDN")
    else:
        print("[+]"+url+" 不存在CDN")


def cdn_r():
    for urls in open('E:/github/scan/dictionary/ip.txt'):
        cdn(urls)