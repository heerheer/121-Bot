import os

import requests

from commands.base.command import ScheduleCommand

global target
global wx

class DailyMoyuReportSchedule(ScheduleCommand):
    def __init__(self):
        # 假设每天早上 12 点执行
        super().__init__('0 12 * * *')

    def match(self, content):
        return content in ['日报','摸鱼日报','摸鱼']

    def handle(self, context):
        # 这里实现每日摸鱼日报的具体逻辑，比如获取数据、生成报告、发送消息等
        url = 'https://api.52vmy.cn/api/wl/moyu' # 摸鱼图片，下载到本地
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            moyu_report = './moyu_report.jpg'
            with open(moyu_report, 'wb') as f:
                f.write(response.content)
            if context is not None:
                context.wx.SendFiles(os.path.abspath(moyu_report), context.source)
            else:
                wx.SendFiles(os.path.abspath(moyu_report), target)  # 假设 wx 和 target 已经正确定义
        except requests.RequestException as e:
            print(f"下载图片时出现错误: {e}")
            if context is not None:
                context.wx.SendMsg('🤡摸鱼日报下载失败!', context.source)
            else:
                wx.SendMsg('🤡摸鱼日报下载失败!', target)  # 假设 wx 和 target 已经正确定义

class DailyGoodMorningSchedule(ScheduleCommand):
    def __init__(self):
        # 假设每天早上 11 点执行
        super().__init__('0 11 * * *')
    def match(self, content):
        return content in ['早报']
    def handle(self, context):
        try:
            url = 'https://api.52vmy.cn/api/wl/60s/new'
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data:list[str] = response.json()['data']
            if context is not None:
                context.quote('\n'.join(data))
            else:
                wx.SendMsg('\n'.join(data), target)
        except requests.RequestException as e:
            print(f"早报出错")


class CrazyKFCSchedule(ScheduleCommand):
    def __init__(self):
        # 假设每天早上 12 点执行
        super().__init__('0 12 * * 4')

    def match(self, content):
        return content in ['疯狂星期四','kfc','KFC','crazy']

    def handle(self, context):
        url = 'https://api.52vmy.cn/api/wl/yan/kfc'
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            kfc = response.json()
            if context is not None:
                context.quote(kfc['content'])
            else:
                wx.SendMsg(kfc['content'], target)
        except requests.RequestException as e:
            print(f"KFC出错")





