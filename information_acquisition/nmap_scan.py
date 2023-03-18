import optparse
import threading

import nmap

tgHost_line = []
tgPort_list = []
success = []


def nmapScan(tgHost):
    for tgPort in tgPort_list:
        nmScan = nmap.PortScanner()
        results = nmScan.scan(tgHost, tgPort)
        state = results['scan'][tgHost]['tcp'][int(tgPort)]['state']
        print("[+] " + tgHost + " tcp/" + tgPort + " " + state)


def nmapscan_r():
    for tgHost in tgHost_line:
        for tgPort in tgPort_list:
            nmScan = nmap.PortScanner()
            results = nmScan.scan(tgHost, tgPort)
            state = results['scan'][tgHost]['tcp'][int(tgPort)]['state']
            port = tgHost + " tcp/" + tgPort + " " + state
            success.append(port + "\n")
            print(tgHost + " tcp/" + tgPort + " " + state)


def read_tgPort():
    for tgPort in open('E:/github/scan/dictionary/port.txt'):
        tgPort = tgPort.replace("\n", "")
        tgPort_list.append(tgPort)


def write(f):
    try:
        for result in success:
            f.write(result)
    except Exception as e:
        print(e)
        pass


def read_tgHost():
    for tgHost in open('E:/github/scan/dictionary/ip.txt'):
        tgHost = tgHost.replace("\n", "")
        tgHost_line.append(tgHost)


def thread_r():
    try:
        with open('E:/github/scan/result/nmap_result.txt', mode='w', encoding='utf-8') as f:
            threads = []
            t1 = threading.Thread(target=read_tgPort)
            threads.append(t1)
            t2 = threading.Thread(target=read_tgHost)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
            threads.append(t2)
            t3 = threading.Thread(target=nmapscan_r)
            threads.append(t3)
            t4 = threading.Thread(target=write, args=(f,))
            threads.append(t4)
            for t in threads:  # 遍历线程列表
                t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
                t.start()
                t.join()
            f.close()
            print("完成扫描")
    except Exception as e:
        print(e)
        pass


def thread(tgHost):
    print("正在进行端口扫描\n")
    threads = []
    t1 = threading.Thread(target=read_tgPort)
    threads.append(t1)
    t2 = threading.Thread(target=nmapScan, args=(tgHost,))
    threads.append(t2)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()

