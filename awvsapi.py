import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import argparse

'''
Full Scan	11111111-1111-1111-1111-111111111111	完全扫描
High Risk Vulnerabilities	11111111-1111-1111-1111-111111111112	高风险漏洞
Cross-site Scripting Vulnerabilities	11111111-1111-1111-1111-111111111116	XSS漏洞
SQL Injection Vulnerabilities	11111111-1111-1111-1111-111111111113	SQL注入漏洞
Weak Passwords	11111111-1111-1111-1111-111111111115	弱口令检测
Crawl Only	11111111-1111-1111-1111-111111111117	Crawl Only
Malware Scan	11111111-1111-1111-1111-111111111120	恶意软件扫描
'''

Awvs_url = 'https://127.0.0.1:3443/' #awvs的访问url
Awvs_api = '1986ad8c0a5b3df4d7028d5f3c06e936cbecb230db07347fa933cd842d573d20c' #awvs中的api
headers = {
    'X-Auth': Awvs_api,
    'Content-type': 'application/json'
}

def addTarget(scan_url):
    info_targets = {"address": scan_url, "description": scan_url, "criticality": "10"}
    r = requests.post(url=Awvs_url + 'api/v1/targets', headers=headers, data=json.dumps(info_targets), verify=False)
    target_id = json.loads(r.content)  # 取出任务id
    return target_id['target_id']

def scanTarget(target_id):
    info_scans = {"target_id": target_id, "profile_id": "11111111-1111-1111-1111-111111111111",
                  "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
    scans_r = requests.post(Awvs_url + "/api/v1/scans", data=json.dumps(info_scans), headers=headers, timeout=30,verify=False)

def linkagescan(target_id):
    info_patch = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "case_sensitive": "yes",
        "proxy": {"enabled": True, "protocol": "http", "address": "10.71.40.94", "port": 7777, "username": "admin", "password": "admin"}}
    scans_r = requests.patch(Awvs_url + "/api/v1/targets/" + target_id['target_id'] + "/configuration",data=json.dumps(info_patch), headers=headers, timeout=30 * 4, verify=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='scan a url')
    parser.add_argument('-f', help='scan a file list')
    parser.add_argument('-x', help='scan a file list coordination xray')
    args = parser.parse_args()
    if (args.u):
        target_id = addTarget(args.u)
        scanTarget(target_id)
        print('成功添加目标：' + args.u)
    if (args.f):
        with open(args.f) as f:
            for i in f:
                url = i.replace("\n", '')
                url = url.replace("\r", '')
                target_id = addTarget(url)
                scanTarget(target_id)
                print('成功添加目标：' + url)
    if (args.x):
        with open(args.x) as f:
            for i in f:
                url = i.replace("\n", '')
                url = url.replace("\r", '')
                target_id = addTarget(url)
                linkagescan(target_id)
                scanTarget(target_id)
                print('成功添加目标：' + url)

