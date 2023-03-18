import json, requests, time
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080"
}  # 代理


# 查看所有目标结果
def targets():
    headers = {
        "X-Auth": apikey,
        "Content-type": "application/json;charset=utf8"
    }
    api_url = tarurl + '/api/v1/targets'
    r = requests.get(url=api_url, headers=headers, verify=False)
    print(r.json())


# 添加targets目标，获取target_id
def post_targets(url):
    headers = {
        "X-Auth": apikey,
        "Content-type": "application/json;charset=utf8"
    }
    api_url = tarurl + '/api/v1/targets'
    data = {
        "address": url,
        "description": "wyt_target",
        "criticality": "10"
    }
    data_json = json.dumps(data)
    r = requests.post(url=api_url, headers=headers, data=data_json, proxies=proxies, verify=False)
    target_id = r.json().get("target_id")
    print('target_id:', target_id)
    return target_id


# 添加scans
def scans(url):
    headers = {
        "X-Auth": apikey,
        "Content-type": "application/json;charset=utf8"
    }
    api_url = tarurl + '/api/v1/scans'
    data = {
        "target_id": url,
        "profile_id": "11111111-1111-1111-1111-111111111111",
        "schedule":
            {
                "disable": False,
                "start_date": None,
                "time_sensitive": False
            }
    }
    data_json = json.dumps(data)
    r = requests.post(url=api_url, headers=headers, data=data_json, proxies=proxies, verify=False)


# 添加generate，并获取generate_id
def generate(url):
    headers = {
        "X-Auth": apikey,
        "Content-type": "application/json;charset=utf8"
    }
    api_url = tarurl + '/api/v1/reports'
    data = {
        "template_id": "11111111-1111-1111-1111-111111111111",
        "source": {
            "list_type": "scans",
            "id_list": [url]
        }
    }
    data_json = json.dumps(data)
    r = requests.post(url=api_url, headers=headers, data=data_json, proxies=proxies, verify=False)


# 获取scan_id，通过start_date可知，最新生成的为第一个
def scan_id():
    headers = {
        "X-Auth": apikey,
        "Content-type": "application/json;charset=utf8"
    }
    api_url = tarurl + '/api/v1/scans'
    r = requests.get(url=api_url, headers=headers, proxies=proxies, verify=False)
    scan_id = r.json().get("scans")[0].get("scan_id")
    print('scan_id:', scan_id)
    return scan_id


def awvs_awvs(url, api):
    print("正在进行awvs扫描，请确保awvs可用，key正确\n" )
    global tarurl, scan_id
    global apikey
    # tarurl = "https://localhost:3443"
    # apikey = "1986ad8c0a5b3df4d7028d5f3c06e936c731c73a0a85f44e4990037db3cd55519"
    tarurl = url
    apikey = api
    for url in open('dictionary/ip.txt'):
        target_id = post_targets(url)
        time.sleep(10)
        scans(target_id)
        scan_id = scan_id()
        generate(scan_id)
