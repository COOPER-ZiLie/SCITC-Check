# -*- coding:utf-8 -*-
"""
@author: Sunshine
@file:Auto_push_main.py
@software:PyCharm
@time:2022/04/01
"""
import requests
import yaml
import time
from bs4 import BeautifulSoup
import schedule
import socket
import random
import string
import os

#随机latitude
latitude1 = random.uniform(32.4410000, 32.4410405)
latitudesj = (round(latitude1, 7) )
#随机longitude
longitude1 = random.uniform(105.895000, 105.895168)
longitudesj = (round(longitude1, 6) )
#随机温度
Temperature1 = random.uniform(36,36.9)
Temperaturesj = (round(Temperature1, 1) )
#随机32位Code
codes1 = ''.join(random.choice(string.ascii_letters + string.digits + string.digits) for _ in range(32))
dtdz = "http://zhcx.scitc.com.cn/weixin/HealthAdd.php?code=" +str(codes1)+ "&state=123"

def send_msg(resp_dict):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '0.0.0.0' #推送go-cqhttp服务器主机地址
    client.connect((host, 5700))  # 端口

    msg_type = resp_dict['msg_type']
    number = resp_dict['number']
    msg = resp_dict['msg']
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + host + "\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + host + ":\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0


def loadYml(ymlFileName='/scitc/SCITC_Auto_push-main/Eyvind/config.yml'):
    with open(ymlFileName, 'r', encoding="utf-8") as file:
        item = yaml.load(file, Loader=yaml.FullLoader)
        return item


def log(log):
    Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(f"{Time}" + "\t" +f"|||{log}|||")
    log = None


def sign(user):
    url_flusheh = 'http://zhcx.scitc.com.cn/weixin/UpdateUserInfor.php'   #可替换为其他API
    #url_get = f"http://zhcx.scitc.com.cn/weixin/HealthAdd.php?code=+codessj+&state=123"
    url_get = dtdz
    url_post = 'http://zhcx.scitc.com.cn/weixin/HealthAdd.php'
    #print(url_get)
    header_flusheh = {
        "Host": "zhcx.scitc.com.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/371 MicroMessenger/8.0.19.2080(0x2800133B) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Referer": url_get,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": user['Cookie'],
    }
    header_get = header_flusheh
    header_post = header_flusheh
    def flusheh():
        try:
            resp_flusheh = requests.get(url_flusheh, headers=header_flusheh)
            log("保持存活ing")
            html_flusheh = resp_flusheh.text
            #print(html_flusheh)
            # soup_flusheh = BeautifulSoup(html_flusheh, 'html.parser')
            # ation = soup_flusheh.find('h4')
            #log(html_flusheh)#debug报表
            # resp_dict = {'msg_type': 'private', 'number': 你和QQ号, 'msg': '用户信息存活'}
            # send_msg(resp_dict)
            #send_msg({'msg_type': 'private', 'number': user['qq_gid'], 'msg': 'Eyvind用户存活'})
        except:
            #send_msg({'msg_type': 'private', 'number': user['qq_gid'], 'msg': 'Eyvind用户信息过期'})
            log("保持存活失败")
    flusheh()#单次运行一次

    def submit():
        def get_value():
            resp_get = requests.get(url_get, headers=header_get)
            html = resp_get.text
            #log(html)
            soup = BeautifulSoup(html, 'html.parser')
            token = "NULL"
            demo = "NULL"
            demo_id = "NULL"
            loadtime = "NULL"
            token = soup.find('input', id='token')["value"]
            demo = soup.find_all('input', type="hidden")[0]["value"]
            demo_id = soup.find_all('input', type="hidden")[0]["id"]
            loadtime = soup.find_all('input', type="hidden")[1]["value"]
            return token, demo, demo_id, loadtime

        parameter = get_value()
        log(parameter)
        IncomingValue = {
            'token': parameter[0],
            'InSchoolYN': 'null',
            'GoOutYN': user['GoOutYN'],
            'Temperature': 'NaN',
            'HealthAction': '正常',
            'HealthMa': 'null',
            'YiMiao_JiaQiang_YN':'null',
            'Other': '',
            'Hesuan24Hours': 'null',
            'LoadTimes': parameter[3],
            'latitude': 'undefined',
            'longitude': 'undefined',
            'speed': 'undefined',
            'accuracy': 'undefined',
            'networkType': 'wifi',
            'Content': '',
            'XinGuanYN': '未感染',
            'XinGuanYiMiao': '第3针',
            # 'yzm': "yzm",
            'action': 'save',
            parameter[2]: parameter[1],
        }
        #print(IncomingValue)
        #resp_post = requests.post(url_post, data=IncomingValue, headers=header_post, timeout=5)
        #str_msg = "智慧川信提醒:" + "\n" + '用户名：' + user['username'] + '\n' + '日期：' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n'
        #txt = str(resp_post.text)
        #str_msg = str_msg + txt[5:16]
        #print(str_msg)
        #send_msg({'msg_type': 'private', 'number': user['qq_gid'], 'msg': str_msg})
        #log(resp_post.text)
    #schedule.every(20).minutes.do(flusheh)  # 保持ck存活刷新时间
    #schedule.every(1).day.at("07:00").do(submit) # 提交打卡时间

def main():
    config = loadYml()
    #print(config)
    for user in config['users']:
        sign(user)


if __name__ == '__main__':
    main()