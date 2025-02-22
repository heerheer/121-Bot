from wxauto import WeChat
# 上下文类
class Context:
    def __init__(self, msg, content, source, wx):
        """
        初始化上下文对象
        :param msg: 消息对象
        :param content: 消息内容
        :param wx: WeChat 对象
        :param source: 群 ID
        """
        self.msg: object = msg
        self.msg: object = msg
        self.wx: WeChat = wx
        self.content: str = content
        self.source: str = source
    def quote(self, message):
        self.msg.quote(message)