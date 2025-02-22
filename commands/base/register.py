# 指令注册器类
from .command import Command

from typing import List


class CommandRegistry:
    def __init__(self):
        self.commands: List[Command] = []

    def register(self, command_obj:Command):
        """
        向命令注册表中注册一个命令对象。

        此方法用于将一个Command类型的对象添加到命令列表中，以便后续可以处理相关命令。

        参数:
        command_obj (Command): 要注册的命令对象，该对象应该实现了Command接口。

        返回:
        无
        """
        # 将传入的命令对象添加到命令列表中
        self.commands.append(command_obj)

    def handle(self, context):
        content = context.content
        for command in self.commands:
            if command.match(content):
                command.handle(context)
                return
        return None

    def start(self):
        for command in self.commands:
            command.start()
