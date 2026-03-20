from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


def get_attraction(city: str, weather: str) -> list[str]:
    """根据城市和天气搜索推荐的旅游景点

    Args:
        city: 城市名称
        weather: 天气描述

    Returns:
        景点推荐列表；失败返回空列表
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return []

        client = TavilyClient(api_key=api_key)
        query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"

        response = client.search(query=query, max_results=5)

        results = []
        for result in response.get("results", []):
            title = result.get("title", "")
            content = result.get("content", "")
            if title and content:
                results.append(f"- {title}: {content}")

        return results
    except Exception:
        return []
