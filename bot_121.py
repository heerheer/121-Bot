from wxauto import WeChat
import time
from auth import Authenticator 
from queryBill import query_electric_bill
import random

from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
username = os.getenv('USER')
password = os.getenv('PASSWORD')

auther = Authenticator('http://202.195.206.214/epay/')
auther.login(username, password)


wx = WeChat()
target = 'C12-121'
wx.AddListenChat(who=target, savepic=False)



# 持续监听消息，并且收到消息后回复“收到”
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who              # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)   # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type       # 获取消息类型
            content = msg.content    # 获取消息内容，字符串类型的消息内容
            if content == '电量':
                if auther.check():
                    wx.SendMsg('当前电量剩余:{:.2f}'.format(query_electric_bill(auther.jsessionid())), target)
                else:
                    auther.login('241210703120','Heershisb996#')
                    wx.SendMsg('当前电量剩余:{:.2f}'.format(query_electric_bill(auther.jsessionid())), target)
            if content == '吴':
                wx.SendMsg(random.choice(['宇杰', '健强','亦凡']),target)
            if content == '王':
                wx.SendMsg(random.choice(['峥涛', '者荣耀']),target)
                
        # ===================================================
        # 处理消息逻辑（如果有）
        # 
        # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
        # 
        # ===================================================
    time.sleep(wait)

