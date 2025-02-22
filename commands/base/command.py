from .context import Context

import re
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# 指令基类
class Command:
    def __init__(self):
        pass

    def match(self, content):
        """
        匹配方法，子类可重写
        :param content: 消息内容
        :return: 是否匹配成功
        """
        return False

    def handle(self, context: Context| None):
        """
        处理方法，子类实现具体逻辑
        :param context: 上下文，包含msg对象、content内容和group群id
        """
        pass

    def start(self):
        pass


# 完全匹配指令类
class ExactMatchCommand(Command):
    def __init__(self, command: str):
        super().__init__()
        self.command = command

    def match(self, content):
        return content == self.command


# 正则匹配指令类
class RegexMatchCommand(Command):
    def __init__(self, pattern):
        super().__init__()
        self.pattern = re.compile(pattern)

    def match(self, content):
        return bool(self.pattern.match(content))


# 含参数匹配指令类
class ParamMatchCommand(Command):
    def __init__(self, command: str):
        super().__init__()
        self.command = command

    def match(self, content):
        return content.startswith(self.command)


# 含参数匹配指令类
class ScheduleCommand(Command):
    def __init__(self, cron):
        super().__init__()
        self.cron = cron
        self.scheduler = BackgroundScheduler()
        self.trigger = CronTrigger.from_crontab(cron)  # 解析cron表达式

    def match(self, content):
        return False

    def start(self):
        self.scheduler.add_job(lambda: self.handle(None) , self.trigger)
        self.scheduler.start()
        print(f"[{self.__class__.__name__}]ScheduleCommand started")


