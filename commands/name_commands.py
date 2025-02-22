from commands.base.command import ExactMatchCommand
import random

class WuCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('吴')

    def handle(self, context):
        context.wx.SendMsg(random.choice(['宇杰', '健强', '亦凡']), context.source)


class WangCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('王')

    def handle(self, context):
        context.wx.SendMsg(random.choice(['峥涛', '者荣耀']), context.source)