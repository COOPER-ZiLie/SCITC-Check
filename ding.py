import autopost    #导入主框架
import subprocess,json,sys,os,datetime
try:
    import requests
except Exception as e:
    subprocess.getstatusoutput('pip install requests -i http://pypi.douban.com/simple  --trusted-host pypi.douban.com')
 
def dingtalk_warning(message):
    webhook = "替换此内容为钉钉通知链接"
    headers = {'Content-Type': 'application/json'}
    data={
        "msgtype": "text",
        "text": {
            "content": message,
        },
        "at": {
        "atMobiles": ["填入你的钉钉手机号"],#如果不想通知全体，请单独@你自己
        "isAtAll": False#是否@全体成员
    }
}
 
    x=requests.post(url=webhook,data=json.dumps(data),headers=headers)
    if x.json()["errcode"] == 0:
        return True
    else:
        return False

def forme():
        if "打卡成功" in autopost.okyn:
            autopost.dingtalk_warning("打卡成功")
        else:
            autopost.dingtalk_warning("打卡失败")
forme()
