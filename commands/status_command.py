import psutil

from commands.base.command import ExactMatchCommand


class StatusCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('当前状态')

    def handle(self, context):
        # 获取 CPU 占用率
        cpu_percent = psutil.cpu_percent(interval=1)
        # 获取内存占用率
        memory_percent = psutil.virtual_memory().percent
        status_msg = f"当前 CPU 占用率: {cpu_percent}%，内存占用率: {memory_percent}%"
        context.wx.SendMsg(status_msg, context.source)