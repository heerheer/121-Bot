import os

from dotenv import load_dotenv

from auth import Authenticator
from commands.base.command import ExactMatchCommand, ScheduleCommand
from queryBill import query_electric_bill

from bot_121 import wx,target

# 加载 .env 文件
load_dotenv()

# 读取环境变量
username = os.getenv('USER')
password = os.getenv('PASSWORD')

auther = Authenticator('http://202.195.206.214/epay/')

if auther.check() is False:
    auther.expire()
    auther.login(username, password)
else:
    print('自动登录成功')

disable_electricity_command = False

if auther.check() is False:
    # 初始化登入失败应该是遇到了网络问题
    print('初始化登录失败...可能是网络环境问题,禁用电费相关指令与计划任务')
    disable_electricity_command = True



# 指令处理类
class ElectricityCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('电量')
        self.auther = auther

    def handle(self, context):
        if disable_electricity_command:
            context.quote('指令暂时不可用')
        if self.auther.check():
            context.quote('当前电量剩余:{:.2f}'.format(query_electric_bill(self.auther.jsessionid())))
        else:
            self.auther.login('241210703120', 'Heershisb996#')
            context.quote('当前电量剩余:{:.2f}'.format(query_electric_bill(self.auther.jsessionid())))


class ElectricityCheckSchedule(ScheduleCommand):
    def __init__(self):
        super().__init__('*/30 * * * *')

    def handle(self, context):
        if disable_electricity_command:
            return
        if auther.check():
            electricity = query_electric_bill(auther.jsessionid())
            if electricity < 30:
                wx.SendMsg('警告：当前电量剩余{:.2f}度，电量低于30度，请及时充值！'.format(electricity), target)
        else:
            auther.login('241210703120', 'Heershisb996#')
            electricity = query_electric_bill(auther.jsessionid())
            if electricity < 30:
                wx.SendMsg('警告：当前电量剩余{:.2f}度，电量低于30度，请及时充值！'.format(electricity), target)
