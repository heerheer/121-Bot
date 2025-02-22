# 项目介绍

## 项目概述
本项目主要利用 `wxauto` 库，结合注册器来管理多个命令与计划任务，同时实现了对 JUST 信息门户的授权、信息获取功能，例如获取宿舍电费信息。此外，还借助 coze 的智能体 API 为用户提供穿搭推荐。

## 功能特性
1. **`wxauto` 库的使用**：通过 `wxauto` 库实现与微信的交互，方便进行自动化操作。
2. **注册器管理**：使用注册器`CommandRegister`来管理多个命令和计划任务，提高系统的可维护性和扩展性。
3. **JUST 信息门户集成**：实现对 JUST 信息门户的授权和信息获取，例如查询宿舍电费。(待完善,目前位于`./auth.py`)
4. **穿搭推荐**：利用 coze 的智能体 API 为用户提供个性化的穿搭推荐。

## 安装与配置
### 安装依赖
```bash
pip install wxauto requests apscheduler python-dotenv
# coze SDK 根据实际使用的API补充安装命令
```

### 环境配置

1. 在项目根目录创建 `.env` 文件：
```ini
# JUST 门户认证
JUST_USERNAME=your_username
JUST_PASSWORD=your_password

# Coze API 配置
COZE_API_KEY=your_api_key
COZE_BOT_ID=your_bot_id

# 微信配置
WX_GROUP_NAME=目标群聊名称
```
## 使用示例
```python
# 命令注册示例
from registry import command_registry, scheduler

@command_registry.register('电费')
async def get_electricity_balance():
    # 获取电费余额的逻辑
    return "当前电费余额：25.6元"

@command_registry.register('穿搭')
async def get_fashion_suggestion():
    # 调用Coze API获取推荐
    return "今日穿搭建议：...（API返回内容）"

# 定时任务注册示例
@scheduler.scheduled_job('cron', hour=8)
def morning_reminder():
    wx.send_msg("记得打卡晨跑哦！", WX_GROUP_NAME)

# 启动监听
wx = WeChat()
wx.listen()
scheduler.start()
```
## 注意事项
1. 使用前需确保微信客户端已登录并授予必要权限
2. JUST 门户接口可能存在调用频率限制
3. 敏感配置信息建议使用环境变量管理
4. 定时任务时间需根据实际需求调整

