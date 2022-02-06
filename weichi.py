import requests
import json
Search_url='http://zhcx.scitc.com.cn/weixin/HealthAdd.php'#登陆网址，只需要抓包一次，如非川信，请替换
Search_par={

}
Search_header={
        'host': 'zhcx.scitc.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'text/html, */*; q=0.01',
        'User-Agent':
            'Mozilla/5.0 (Linux; Android 10; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3117 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/371 MicroMessenger/8.0.11.1960(0x28000B33) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://zhcx.scitc.com.cn',#如非川信，请替换
        'Referer': 'http://zhcx.scitc.com.cn/weixin/HealthAdd.php',#如非川信，请替换
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cookie': 'PHPSESSID=填写最新的cookies',  # 登录信息，保持和auto-check.py一致
}
r1 = requests.get(Search_url,data=json.dumps(Search_par),headers=Search_header)
r2 = (r1.text)
#在发送请求的时候带上了上一个对话的cookie
#print(r2)
def check():
    if "<html>" in r2:
        print ("xxx-维持成功！")
    else:
        print ("xxx-维持失败！！！")
check()
