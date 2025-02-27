from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import requests
from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL,ChatEventType,Message

def get_origin(url):
    parsed_url = urlparse(url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return origin
def get_host_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc  # 返回主机名（Host）

load_dotenv()
bot_id = "7474184451287908378"
user_id = "123"
# 通过环境变量引入密钥，访问 coze.cn 服务
coze = Coze(auth=TokenAuth(os.getenv("COZE_KEY")), base_url=COZE_CN_BASE_URL)

# 和风天气 API 配置
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://devapi.qweather.com/v7/weather/now"
WEATHER_API_LOCATION = "101190306"  # 京口区的位置编码
def get_temp_now():
    """
    获取当前天气信息
    """
    params = {
        "key": WEATHER_API_KEY,
        "location": WEATHER_API_LOCATION  # 京口区的位置编码
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_text = data["now"]["text"]
        temperature = data["now"]["temp"]
        return temperature
    return 999

def get_weather()->str:
    """
    获取当前天气信息
    """
    FORECAST_API_URL = "https://devapi.qweather.com/v7/weather/3d"  # 3天预报API
    params = {
        "key": WEATHER_API_KEY,
        "location": WEATHER_API_LOCATION
    }
    response = requests.get(FORECAST_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        today = data["daily"][0]  # 获取今天的数据
        weather_text = today["textDay"]  # 白天天气状况
        temp_max = today["tempMax"]  # 最高温度
        temp_min = today["tempMin"]  # 最低温度
        return f"天气：{weather_text}，最高温度：{temp_max}℃，最低温度：{temp_min}℃"
    return "无法获取天气信息"



def get_three_days_weather()->str:
    """获取未来三天的天气预报信息"""
    FORECAST_API_URL = "https://devapi.qweather.com/v7/weather/3d"  # 3天预报API
    params = {
        "key": WEATHER_API_KEY,
        "location": WEATHER_API_LOCATION
    }
    response = requests.get(FORECAST_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast_text = ""
        for i, day in enumerate(data["daily"]):
            day_text = "今天" if i == 0 else "明天" if i == 1 else "后天"
            forecast_text += f"{day_text}：{day['textDay']}，气温{day['tempMin']}℃~{day['tempMax']}℃\n"
        return forecast_text.strip()
    return "无法获取天气预报信息"

def get_outfit_recommendation(weather,style="简约",loc="学校"):
    """
    根据天气信息调用大模型获取穿搭推荐
    """
    prompt = f'''
    今天的天气是 {weather}，请推荐今日的穿搭(主要以适合温度为主，兼具保暖与美观，不要细节描述颜色与款式，回复不要过于详细)
    风格：{style}
    出行场合：{loc}
    '''
    response = coze.chat.stream(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[
           Message.build_user_question_text(prompt)
        ],
        auto_save_history=False
    )
    answer = ""
    for event in response:
        if event.event == ChatEventType.CONVERSATION_MESSAGE_COMPLETED and event.message.type == "answer":
            answer = event.message.content
    return answer

def get_air_quality():
    """
    获取当前空气质量信息
    """
    AIR_QUALITY_API_URL = "https://devapi.qweather.com/v7/air/now"
    params = {
        "key": WEATHER_API_KEY,
        "location": WEATHER_API_LOCATION  # 京口区的位置编码
    }
    response = requests.get(AIR_QUALITY_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        aqi = data["now"]["aqi"]  # 空气质量指数
        category = data["now"]["category"]  # 空气质量等级
        return f"空气质量指数：{aqi}，等级：{category}"
    return "无法获取空气质量信息"