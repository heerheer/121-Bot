import os

from dotenv import load_dotenv

from auth import Authenticator
from commands.base.command import ExactMatchCommand, ScheduleCommand
from queryBill import query_electric_bill

global wx
global target

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


# 指令处理类
class ElectricityCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('电量')
        self.auther = auther

    def handle(self, context):
        if self.auther.check():
            context.wx.SendMsg('当前电量剩余:{:.2f}'.format(query_electric_bill(self.auther.jsessionid())),
                               context.source)
        else:
            self.auther.login('241210703120', 'Heershisb996#')
            context.wx.SendMsg('当前电量剩余:{:.2f}'.format(query_electric_bill(self.auther.jsessionid())),
                               context.source)


class ElectricityCheckSchedule(ScheduleCommand):
    def __init__(self):
        super().__init__('*/30 * * * *')

    def handle(self, context):
        if auther.check():
            electricity = query_electric_bill(auther.jsessionid())
            if electricity < 30:
                wx.SendMsg('警告：当前电量剩余{:.2f}度，电量低于30度，请及时充值！'.format(electricity), target)
        else:
            auther.login('241210703120', 'Heershisb996#')
            electricity = query_electric_bill(auther.jsessionid())
            if electricity < 30:
                wx.SendMsg('警告：当前电量剩余{:.2f}度，电量低于30度，请及时充值！'.format(electricity), target)
