import requests
from dotenv import load_dotenv

load_dotenv()

CITY_MAPPING = {
    "北京": "Beijing",
    "上海": "Shanghai",
    "广州": "Guangzhou",
    "深圳": "Shenzhen",
    "杭州": "Hangzhou",
    "南京": "Nanjing",
    "成都": "Chengdu",
    "重庆": "Chongqing",
    "武汉": "Wuhan",
    "西安": "Xi'an",
    "苏州": "Suzhou",
    "天津": "Tianjin",
    "长沙": "Changsha",
    "青岛": "Qingdao",
    "大连": "Dalian",
}


def get_weather(city: str) -> str:
    """查询指定城市的实时天气

    使用 Open-Meteo 免费天气 API，支持地理编码和天气查询

    Args:
        city: 城市名称（支持中文和英文）

    Returns:
        天气描述字符串，如"晴天 25°C"；失败返回空字符串
    """
    try:
        english_city = CITY_MAPPING.get(city, city)

        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={english_city}&count=1&language=en&format=json"
        geocode_response = requests.get(geocode_url, timeout=10)

        if geocode_response.status_code != 200:
            return ""

        geocode_data = geocode_response.json()
        results = geocode_data.get("results", [])

        if not results:
            return ""

        latitude = results[0].get("latitude")
        longitude = results[0].get("longitude")
        name = results[0].get("name", city)

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url, timeout=10)

        if weather_response.status_code != 200:
            return ""

        weather_data = weather_response.json()
        current = weather_data.get("current_weather", {})

        temperature = current.get("temperature", 0)
        weather_code = current.get("weathercode", 0)

        weather_desc = get_weather_description(weather_code)

        return f"{name} {weather_desc} {temperature}°C"

    except requests.RequestException:
        return ""


def get_weather_description(code: int) -> str:
    """将天气代码转换为描述文字

    Args:
        code: WMO 天气代码

    Returns:
        天气描述字符串
    """
    weather_codes = {
        0: "晴天",
        1: "多云",
        2: "阴天",
        3: "阴天",
        45: "雾",
        48: "雾",
        51: "小雨",
        53: "小雨",
        55: "小雨",
        61: "中雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "小雪",
        75: "大雪",
        80: "阵雨",
        81: "阵雨",
        82: "暴雨",
        95: "雷雨",
        96: "雷雨",
        99: "雷雨",
    }

    return weather_codes.get(code, "多云")
