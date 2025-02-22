import time

from wxauto import WeChat
from commands import * # 导入所有命令

global wx
global target

wx = WeChat()
target = 'C12-121'

# 初始化指令注册器
registry = CommandRegistry()
registry.register(ElectricityCommand())
registry.register(WuCommand())
registry.register(WangCommand())
registry.register(StatusCommand())
registry.register(HelpCommand())
registry.register(WeatherCommand())
registry.register(ElectricityCheckSchedule())
registry.register(DailyMoyuReportSchedule())
registry.register(CrazyKFCSchedule())
registry.register(DailyGoodMorningSchedule())

wx.AddListenChat(who=target, savepic=False)
wx.AddListenChat(who='bottest', savepic=False)

wait = 1  # 设置1秒查看一次是否有新消息
check_interval = 30 * 60  # 设置30分钟的检测间隔，单位为秒
last_check_time = time.time()


registry.start()

# 开始监听消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who  # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)  # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            ctx = Context(msg=msg, content=msg.content, source=chat.who, wx=wx)
            msgtype = msg.type  # 获取消息类型   # 获取消息内容，字符串类型的消息内容
            registry.handle(ctx)
    time.sleep(wait)
