# 项目介绍

## 项目概述
本项目主要利用 `wxauto` 库，结合注册器来管理多个命令与计划任务，同时实现了对 JUST 信息门户的授权、信息获取功能，例如获取宿舍电费信息。此外，还借助 coze 的智能体 API 为用户提供穿搭推荐。

## 功能特性
1. **`wxauto` 库的使用**：通过 `wxauto` 库实现与微信的交互，方便进行自动化操作。
2. **注册器管理**：使用注册器`CommandRegister`来管理多个命令和计划任务，提高系统的可维护性和扩展性。
3. **JUST 信息门户集成**：实现对 JUST 信息门户的授权和信息获取，例如查询宿舍电费。(待完善,目前位于`./auth.py`)
4. **天气与穿搭推荐**：使用和风天气API获取精准的数据，利用 coze 的智能体 API 为用户提供个性化的穿搭推荐。

## 安装与配置
### 安装依赖
```bash
pip install wxauto requests apscheduler python-dotenv
```

### 环境配置

1. 在项目根目录创建 `.env` 文件：
```ini
# JUST 门户认证
USER=your_username
JUST_PASSWORD=your_password

# Coze API 配置
COZE_KEY=your_api_key

# 和风天气
WEATHER_API_KEY=your_weather_api_key
```
## 使用示例

`help_command.py`文件
```python
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
```
入口文件`main.py`
```python
from commands import * #获取所有依赖的Command相关类
registry = CommandRegistry()
registry.register(HelpCommand())
```
## Command
### ExactMatchCommand
`ExactMatchCommand` 是一个用于精确匹配消息内容的命令类。当收到的消息内容与命令的关键词完全匹配时，该命令将被触发。
### RegexMatchCommand
`RegexMatchCommand` 是一个用于正则表达式匹配消息内容的命令类。当收到的消息内容与命令的正则表达式匹配时，该命令将被触发。
### ParamMatchCommand
`ParamMatchCommand` 是一个用于参数匹配的命令类。当收到的消息内容与命令的参数匹配时，该命令将被触发。
### ScheduleCommand
`ScheduleCommand` 是一个用于定时触发的命令类。它默认只可以从 cron 表达式来触发命令的执行，此时`context`为`None`，需要使用`global`的`wx`与`target`变量。
- 也可以覆写match使得其能够被消息触发，但注意，`context`此时不为`None`
## 注意事项
1. 使用前需确保微信客户端已登录并授予必要权限
2. JUST 门户接口可能存在调用频率限制
3. 敏感配置信息建议使用环境变量管理
4. 定时任务时间需根据实际需求调整

