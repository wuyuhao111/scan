import optparse
import threading
from concurrent.futures import ThreadPoolExecutor
import nmap

tgHost_line = []
tgPort_list = []
success = []

lock = threading.Lock()


def nmapScan(tgPort, tgHost):
    try:
        nmScan = nmap.PortScanner()
        results = nmScan.scan(tgHost, tgPort)
        state = results['scan'][tgHost]['tcp'][int(tgPort)]['state']
        success.append("[+] " + tgHost + " tcp/" + tgPort + " " + state + "\n")
        print(tgHost + " tcp/" + tgPort + " " + state)
    except Exception as e:
        print(e)
        pass


def read_tgPort():
    try:
        for tgPort in open('E:/github/scan/dictionary/port.txt'):
            tgPort = tgPort.replace("\n", "")
            tgPort_list.append(tgPort)
    except Exception as e:
        print(e)
        pass


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
    print("完成")


def read_tgHost():
    try:
        for tgHost in open('E:/github/scan/dictionary/ip.txt'):
            tgHost = tgHost.replace("\n", "")
            tgHost_line.append(tgHost)
    except Exception as e:
        print(e)
        pass


def thread_r():
    threads = []
    t1 = threading.Thread(target=read_tgPort)
    threads.append(t1)
    t2 = threading.Thread(target=read_tgHost)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t2)
    t3 = threading.Thread(target=information_r)
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


def thread(tgHost):
    print("正在进行端口扫描\n")
    threads = []
    try:
        t1 = threading.Thread(target=read_tgPort())
        threads.append(t1)
        t2 = threading.Thread(target=information, args=(tgHost,))
        threads.append(t2)
        t3 = threading.Thread(target=write)
        threads.append(t3)
        for t in threads:  # 遍历线程列表
            t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
            t.start()
            t.join()
    except Exception as e:
        print(e)
        pass


def information(tgHost):
    try:
        tgPort = tgPort_list
        with ThreadPoolExecutor(max_workers=50) as executor:
            for port in tgPort:
                try:
                    executor.submit(nmapScan, port.strip(), tgHost)
                except Exception as e:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        pass


def information_r():
    try:
        tgPort = tgPort_list
        tgHost = tgHost_line
        with ThreadPoolExecutor(max_workers=50) as executor:
            for tgHost in tgHost:
                for tgPort in tgPort:
                    try:
                        executor.submit(nmapScan, tgPort.strip(), tgHost.strip())
                    except Exception as e:
                        print(e)
                        pass
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    thread("127.0.0.1")
