from commands.base.command import ExactMatchCommand
from utils import get_weather, get_outfit_recommendation, get_air_quality, get_temp_now


class WeatherCommand(ExactMatchCommand):
    def __init__(self):
        super().__init__('天气')

    def handle(self, ctx):
        ctx.quote("⌛正在查询今日天气与AI穿搭建议...")
        weather = get_weather()
        outfit_recommendation = get_outfit_recommendation(weather)
        message = (f"👀{weather}\n"
                   f"🌡️当前温度:{get_temp_now()}℃\n"
                   f"🌫️{get_air_quality()}\n"
                   f"🧥穿搭推荐：\n{outfit_recommendation}")
        ctx.quote(message)