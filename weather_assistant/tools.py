from .weather import get_weather
from .attractions import get_attraction

TOOLS = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

TOOL_DESCRIPTIONS = {
    "get_weather": "查询指定城市的实时天气",
    "get_attraction": "根据城市和天气搜索推荐的旅游景点",
}

__all__ = ["get_weather", "get_attraction", "TOOLS", "TOOL_DESCRIPTIONS"]
