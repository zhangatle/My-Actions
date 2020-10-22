import requests
import sys;
sys.path.append("My-Actions/function/")
from bilibili import *
import time
import os

msg = ""

serverJ = os.environ['push_key']
# 尝试登陆
b = Bilibili()
b.login(username=os.environ['BILI_USER'], password=os.environ['BILI_PASS'])

# 获取 Cookie
cookie_str = ""
cookies = b.get_cookies()
for cookie in cookies:
    cookie_str += cookie + "=" + cookies[cookie] + "; "

headers_with_cookie={
    'User-Agent': "Mozilla/5.0 BiliDroid/6.4.0 (bbcallen@gmail.com) os/android model/M1903F11I mobi_app/android build/6040500 channel/bili innerVer/6040500 osVer/9.0.0 network/2",
    'Cookie': cookie_str
}

print("哔哩哔哩漫画开始签到 start>>>")
msg = msg + "哔哩哔哩漫画开始签到: \n"

r = requests.post("https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn", verify=False, headers=headers_with_cookie, data={
    "platform": "android"
})

# print("响应: " + r.text)
if r.json()['code'] == 0:
    print("签到成功.")
    msg = msg + "签到成功🐶\n"
if r.json()['msg'] == "clockin clockin is duplicate":
    print("今日已签到.")
    msg = msg + "今日已签到⚠\n"

time.sleep(2)

print("哔哩哔哩漫画获取签到信息 start>>>")
msg = msg + "哔哩哔哩漫画获取签到信息: \n"
r = requests.post("https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo", verify=False, headers=headers_with_cookie)

print("累计签到" + str(r.json()['data']['day_count']) + "天🐶")
msg = msg + "累计签到" + str(r.json()['data']['day_count']) + "天🐶\n"

time.sleep(3)

print("哔哩哔哩银瓜子兑换硬币 start>>>")
print(b.silver_to_coin())

# print(msg)

# Server酱
if serverJ != "":
    api = "https://sc.ftqq.com/"+ serverJ + ".send"
    title = u"哔哩哔哩漫画签到"
    content = msg
    data = {
        "text":title,
        "desp":content
    }
    req = requests.post(api,data = data)
