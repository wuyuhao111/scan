import os

def see_see_your_waf(url):
    print("正在进行waf识别\n")
    os.system("python ../scan/wafw00f/wafw00f/main.py " + url)

def see_see_your_waf_r():
    for urls in open('../dictionary/ip.txt'):
        os.system("python ../wafw00f/wafw00f/main.py " + urls)