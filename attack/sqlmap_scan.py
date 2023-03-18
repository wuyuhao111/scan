import requests, json, time


def sqlmapapi(ip):
    # 扫描的网址信息
    data = {
        'url': ip
    }

    # 请求头
    header = {
        'Content-Type': 'application/json'
    }

    # 1.创建任务id
    test_new_url = 'http://127.0.0.1:8775/task/new'
    resp = requests.get(test_new_url)  # 请求接口
    test_id = resp.json()['taskid']  # 获取接口id
    if 'success' in resp.content.decode('utf-8'):
        print('[+]sqlmapapi 任务创建成功')

        # 2.设置任务id的配置信息（扫描信息）
        test_set_url = 'http://127.0.0.1:8775/option' + test_id + '/set'
        test_set_resp = requests.post(test_set_url, data=json.dumps(data), headers=header)  # 扫描信息
        if 'success' in test_set_resp.content.decode('utf-8'):
            print('[+]sqlmapapi 设置成功')

            # 3.启动对应ID的扫描任务
            test_start_url = 'http://127.0.0.1:8775/scan' + test_id + '/start'
            test_start_resp = requests.post(test_set_url, data=json.dumps(data), headers=header)
            if 'success' in test_start_resp.content.decode('utf-8'):
                print('[+]sqlmapapi 配置成功')

                while 1:
                    # 4.读取对应ID的扫描状态
                    test_starts_url = 'http://127.0.0.1:8775/scan' + test_id + '/status'
                    test_starts_resp = requests.get(test_starts_url)
                    if 'running' in test_starts_resp.content.decode('utf-8'):
                        print('[-]' + ip + '| 正在扫描中')
                    else:
                        print('[+]成功')
                        test_data_url = 'http://127.0.0.1:8775/scan' + test_id + '/data'
                        test_data_resp = requests.get(test_data_url).content.decode('utf-8')
                        with open(r'result/sqlmap_reulte.txt', 'a+') as f:  # 写入存在sql注入的结果
                            f.write(id + '\n')
                            f.write(test_data_resp + '\n')  # 注入情况
                            f.write('********************************************************************************')
                            f.close()
                        test_deltack_url = 'http://127.0.0.1:8775/tesk' + test_id + '/delete'  # 删除节省资源
                        test_deltack = requests.get(test_deltack_url)
                        if 'success' in test_deltack.content.decode('utf-8'):
                            print('删除id成功')
                        break
                    time.sleep(3)


def sqlmap_r():
    for ip in open('dictionary/sql.txt'):
        ip = ip.replace('\n', '')
        sqlmapapi(ip)


def sqlmap(ip):
    print("正在调用sqlmap api，请确保可用")
    sqlmapapi(ip)