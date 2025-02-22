from commands.base.command import ExactMatchCommand


class HelpCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('帮助')

    def handle(self, context):
        help_msg = "你可以发送以下命令来获取信息：\n"
        help_msg += "- '电量'：获取当前C12-121宿舍电量剩余量\n"
        help_msg += "- '当前状态'：获取当前 CPU 和内存占用率\n"
        help_msg += "- '日报：获取今日摸鱼日报\n"
        help_msg += "- '天气'：获取今日天气与穿搭推荐\n"
        help_msg += "- '帮助'：显示此帮助信息\n"
        context.msg.quote(help_msg)