import requests,re

def aizhan(ur):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0;  http://www.baidu.com/search/spider.html)'
    }
    # pr = {
    #     'http' : 'http://127.0.0.1:10809'
    # }
    f = open('./ok.txt','w',encoding='utf-8')
    # s = 0
    try:
        for i in range(1,60):
            url = 'https://dns.aizhan.com/' + ur + '/{0}/'.format(str(i))
            print(url)
            res = requests.get(url=url,headers=headers)
            res.encoding = 'utf-8'
            html = res.text
            if '格式错误!' in html:
                print('格式错误! 无此url！')
                break
            elif '根据相关规定，结果未予显示！' in html:
                print('根据相关规定，结果未予显示！')
                continue
            elif '暂无域名解析到该IP' in html:
                print('采集完成！')
                break

            pang = re.findall('rel="nofollow" target="_blank">(.*)</a>',html)
            for urls in pang:
                if '-' in urls:
                    continue
                else:
                    f.write(urls + '\n')
                    # s += 1
                    # print(s)


    except Exception as e:
        print(e)

    finally:
        f.close()

if __name__ == '__main__':
    ur = input('请输入要查询旁站的url:')
    aizhan(ur)
