import re
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from rich import print
from rich.prompt import Prompt

from .tools import TOOLS, TOOL_DESCRIPTIONS


def load_config():
    """加载环境变量配置"""
    load_dotenv()

    config = {
        "tavily_api_key": os.getenv("TAVILY_API_KEY"),
        "ollama_api_key": os.getenv("OLLAMA_API_KEY"),
        "agent_system_prompt": os.getenv("AGENT_SYSTEM_PROMPT"),
        "model_name": os.getenv("MODEL_NAME", "qwen3.5"),
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
    }

    return config


def parse_agent_response(response: str) -> tuple[str, str]:
    """解析 Agent 输出的 Thought 和 Action

    Args:
        response: 大模型返回的文本

    Returns:
        (thought, action) 元组
    """
    thought_match = re.search(r"Thought:\s*(.+?)(?=\nAction:|\Z)", response, re.DOTALL)
    action_match = re.search(r"Action:\s*(.+?)(?=\n)", response, re.DOTALL)

    thought = thought_match.group(1).strip() if thought_match else ""
    action = action_match.group(1).strip() if action_match else ""

    if not action:
        action_match = re.search(r"Action:\s*(.+?)$", response, re.DOTALL)
        action = action_match.group(1).strip() if action_match else ""

    return thought, action


def parse_action(action: str) -> tuple[str, dict]:
    """解析 Action 字符串，提取函数名和参数

    Args:
        action: Action 行内容，如 get_weather(city="北京")

    Returns:
        (function_name, args_dict) 元组
    """
    if action.startswith("Finish"):
        return "finish", {"result": action}

    match = re.match(r"(\w+)\(([^)]*)\)", action)
    if not match:
        return "", {}

    func_name = match.group(1)
    args_str = match.group(2)

    args_dict = {}
    if args_str:
        arg_matches = re.findall(r'(\w+)="([^"]+)"', args_str)
        for key, value in arg_matches:
            args_dict[key] = value

    return func_name, args_dict


def execute_action(func_name: str, args: dict, context: dict):
    """执行工具函数或返回 Finish 结果

    Args:
        func_name: 函数名
        args: 参数字典
        context: 当前上下文（包含 city, weather 等信息）

    Returns:
        工具执行结果或 Finish 标记
    """
    if func_name == "finish":
        return args.get("result", "")

    if func_name in TOOLS:
        func = TOOLS[func_name]
        try:
            if func_name == "get_weather":
                city = args.get("city", context.get("city", ""))
                return func(city)
            elif func_name == "get_attraction":
                city = args.get("city", context.get("city", ""))
                weather = args.get("weather", context.get("weather", ""))
                return func(city, weather)
        except Exception:
            return ""

    return ""


def run_agent_loop(city: str, config: dict):
    """运行 Agent 循环

    Args:
        city: 城市名称
        config: 配置字典

    Returns:
        最终推荐结果
    """
    client = OpenAI(
        base_url=config["ollama_base_url"], api_key=config["ollama_api_key"]
    )

    context = {"city": city, "weather": "", "attractions": [], "messages": []}

    system_prompt = config["agent_system_prompt"] or ""

    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        user_message = f"城市：{city}"
        if context["weather"]:
            user_message += f"\n天气：{context['weather']}"
        if context["attractions"]:
            user_message += f"\n景点信息已收集"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        try:
            response = client.chat.completions.create(
                model=config["model_name"], messages=messages
            )

            content = response.choices[0].message.content or ""

            thought, action = parse_agent_response(content)

            print(f"\n[bold blue]Thought:[/bold blue] {thought}")
            print(f"[bold green]Action:[/bold green] {action}")

            func_name, args = parse_action(action)

            if func_name == "finish":
                result = args.get("result", "")
                result = result.replace("Finish[", "").replace("]", "")
                return result

            result = execute_action(func_name, args, context)

            if func_name == "get_weather":
                context["weather"] = result
                print(f"[bold yellow]天气查询结果:[/bold yellow] {result}")
            elif func_name == "get_attraction":
                context["attractions"] = result
                print(f"[bold yellow]景点搜索结果:[/bold yellow] 共 {len(result)} 条")

        except Exception as e:
            print(f"[bold red]错误:[/bold red] {e}")
            break

    return "抱歉，无法生成推荐，请重试。"


def main():
    """主入口函数"""
    # 修复 Windows 控制台中文乱码
    if sys.platform == "win32":
        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

    print("[bold magenta]=== 智能旅行助手 ===[/bold magenta]")

    config = load_config()

    try:
        city = Prompt.ask("[bold cyan]请输入城市名称[/bold cyan]")
    except EOFError:
        print("[bold red]输入错误，请重试[/bold red]")
        return

    if not city:
        print("[bold red]城市名称不能为空[/bold red]")
        return

    print(f"\n[bold]正在查询 {city} 的天气和景点推荐...[/bold]\n")

    result = run_agent_loop(city, config)

    print(f"\n[bold magenta]=== 推荐结果 ===[/bold magenta]")
    print(result)


if __name__ == "__main__":
    main()
