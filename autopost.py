import requests
import json
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

class Smtp:
    '''邮箱推送类'''

    def __init__(self, host, user, key, sender, receivers):
        self.host = host
        self.user = user
        self.key = key
        self.sender = sender
        self.receivers = receivers
        self.configIsCorrect = self.isCorrectConfig()

    def isCorrectConfig(self):
        # 简单检查邮箱地址或API地址是否合法
        if type(self.receivers) != list:
            return 0
        for item in [self.host, self.user, self.key, self.sender
                     ] + self.receivers:
            if not type(item) == str:
                return 0
            if len(item) == 0:
                return 0
            if "*" in item:
                return 0
        return 1

    def sendmail(self, msg, title):
            mail = MIMEText(msg, 'plain', 'utf-8')
            mail['Subject'] = Header(title, 'utf-8')

            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.host, 587)
            #smtpObj.set_debuglevel(1)#邮件DeBug模式
            smtpObj.login(self.user, self.key)
            smtpObj.sendmail(self.sender, self.receivers, mail.as_string())
            print("邮件发送成功")
        #else:
        #    print('邮件配置出错')
        #    return '邮件配置出错'

#单独负责捕获最新的Token
Search_url='http://zhcx.scitc.com.cn/weixin/HealthAdd.php'#登陆网址，只需要抓包一次，如非川信，请替换
Search_header2={
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
        'Cookie': 'PHPSESSID=d6sfg5rodpea4l5s9l3f4v0oe3',  # 登录信息，保持和weichi.py一致
}
#查询并获取最新的token
login = requests.get(Search_url,headers=Search_header2)
gettoken=re.search(r'("token" value=")(.*?)(" />)',login.text)
numtoken=re.findall('value="(.+?)"', str(gettoken))
#表单主体内容，博主写于寒假期间，请按照自己的需求更改！
Search_par={
        'token': [numtoken[0]],
        'InSchoolYN': '不在校',#是否在校
        'GoOutYN': '不在广元，在省内',#是否离省
        'Temperature': '36',#当前体温
        'Infor': '',
        'HealthAction': '正常',#是否感冒
        'HealthMa': '绿码',#健康码状态
        'Other': '',
        'latitude': '32.4410501',#这是定位信息
        'longitude': '105.895199',
        'speed': '0.0',
        'accuracy': '15.0',
        'networkType': 'wifi',#什么网络下提交的
        'Content': '',
        'action': 'save',

}
#负责最后的提交
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
        'Cookie': 'PHPSESSID=d6sfg5rodpea4l5s9l3f4v0oe3',  # 登录信息，保持和weichi.py一致
}
#print(numtoken[0])#监视根据HTML获得的token
r1 = requests.post(Search_url,data=Search_par,headers=Search_header)#在发送请求的时候带上了上一个对话的cookie
okyn = (r1.text)
import subprocess,json,sys,os,datetime

#print(okyn)#DeBug模式
def emails():
    if "打卡成功" in okyn:
        #print("打卡成功！")
        sendStr = '日期：' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + f'{r1.text}' + '\n'
        print(sendStr)
        print("正在发送邮件...")
        Smtp('smtp.qq.com', '默认qq发送邮件提醒，登陆名', '在mail里获取到的授权码', '再次重复登录名', '邮件接收地址').sendmail(sendStr,'智慧川信公众号签到情况')
        r1.close()
    else:
        print("出错了！请检查并开启DeBug模式！！！")
emails()