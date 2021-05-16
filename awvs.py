import requests
import hashlib
import json
import argparse

username = 'admin@admin.com' #修改你的账号
password = 'aascom@123'          #修改你的密码
awvs_url = 'https://localhost:3443/'#路径

class Awvs():
    awvs = ''
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    def __init__(self, awvs_url, username, password):
        self.awvs_url = awvs_url
        password = hashlib.sha256(password.encode()).hexdigest()
        info = {
            "email": username,
            "password": password,
            "remember_me": "false",
            "logout_previous":"true"
        }
        info = json.dumps(info)
        requests.packages.urllib3.disable_warnings()
        r = requests.session()
        text = r.post(url = awvs_url + 'api/v1/me/login', data=info, verify=False, headers=self.headers)
        print(text.status_code)
        try:
            X_Auth = r.post(self.awvs_url + 'api/v1/me/login', data=info, verify=False, headers=self.headers).headers['X-Auth']
        except:
            exit('awvs Login failed')
        self.headers['X-Auth'] = X_Auth
        self.awvs = r
    
    def addTarget(self,target_url):
        info = {"targets":[{"address": target_url,"description":""}],"groups":[]}
        info = json.dumps(info)
        ret = self.awvs.post(self.awvs_url + '/api/v1/targets/add', data=info, verify=False, headers=self.headers).text
        ret = json.loads(ret)
        target_id = ret['targets'][0]['target_id']

        self.awvs.delete(self.awvs_url + 'api/v1/targets/' + target_id +'/configuration/client_certificate', verify=False, headers=self.headers)

        info1 = {
            "description":"",
            "criticality":10
         }
        info1 = json.dumps(info1)
        self.awvs.patch(self.awvs_url + 'api/v1/targets/' + target_id, data=info1,verify=False, headers=self.headers)

        info2 = {"default_scanning_profile_id":"11111111-1111-1111-1111-111111111111","user_agent":"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)","proxy":{"enabled":True,"protocol":"http","address":"127.0.0.1","port":10809}}  #,"proxy":{"enabled":True,"protocol":"http","address":"127.0.0.1","port":10809}
        info2 = json.dumps(info2)
        self.awvs.patch(self.awvs_url + 'api/v1/targets/' + target_id + '/configuration', data=info2, verify=False, headers=self.headers)

        return target_id

    def addList(self, target_url):
        info = {"targets":[{"address": target_url,"description":""}],"groups":[]}
        info = json.dumps(info)
        ret = self.awvs.post(self.awvs_url + '/api/v1/targets/add', data=info, verify=False, headers=self.headers).text
        ret = json.loads(ret)
        target_id = ret['targets'][0]['target_id']
        return target_id

    def scanTarget(self, target_id):
        false=False
        null=None
        scaninfo = {"profile_id":"11111111-1111-1111-1111-111111111111","ui_session_id":"0190f88f0c88f3bc6063a7fc657f52f7","incremental":false,"schedule":{"disable":false,"start_date":null,"time_sensitive":false},"target_id": target_id}
        scaninfo = json.dumps(scaninfo)
        self.awvs.post(self.awvs_url+'/api/v1/scans',data=scaninfo, verify=False, headers=self.headers)
        

    def getScanList(self):
        scan_list= self.awvs.get(self.awvs_url + "/api/v1/scans?l=100", verify=False, headers=self.headers).text
        scan_list = json.loads(scan_list)
        scan_lists = []
        for i in scan_list['scans']:
            scan_lists.append(i['scan_id'])
        return scan_lists

    def getTargetList(self):
        target_list = self.awvs.get(self.awvs_url + "/api/v1/targets?l=100", verify=False, headers=self.headers).text
        target_list = json.loads(target_list)
        target_lists = []
        for i in target_list['targets']:
            target_lists.append(i['target_id'])
        return target_lists


    def delTarget(self, target_id):
        self.awvs.delete(self.awvs_url + "/api/v1/targets/" + target_id, verify=False, headers=self.headers)


    def delScan(self, scan_id):
        self.awvs.delete(self.awvs_url + "/api/v1/scans/" + scan_id, verify=False, headers=self.headers)
    
if __name__ == "__main__":
    awvs = Awvs(awvs_url, username, password)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='scan a file list')
    parser.add_argument('-x',help='scan a file list coordination xray')
    parser.add_argument('-d',action='store_true',help='delete all target and scan')
    args = parser.parse_args()

    if (args.x):
        with open(args.x) as f:
            for i in f:
                url = i.replace("\n", '')
                url = url.replace("\r", '')
                target_id = awvs.addTarget(url)
                awvs.scanTarget(target_id)
                print('starting scan ' + url)

    if (args.f):
        with open(args.f) as f:
            for i in f:
                url = i.replace("\n", '')
                url = url.replace("\r", '')
                target_id = awvs.addList(url)
                if len(target_id) > 10:
                    awvs.scanTarget(target_id)
                    print('starting scan ' + url)
                else:
                    continue
    if (args.d):
        scan_list = awvs.getScanList()
        target_list = awvs.getTargetList()
        for i in scan_list:
            awvs.delScan(i)
        for i in target_list:
            awvs.delTarget(i)
        print('all delete success')