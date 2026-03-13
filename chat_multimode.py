"""
Ollama Cloud API方式 多模态对话脚本(需自行申请 Ollama API Key)
支持文本对话 + 图片理解，Rich 美化输出
"""

import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv
from ollama import Client
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box

# ==================== 配置区域 ====================

# 项目根目录
PROJECT_ROOT = Path(r"E:\python\ai-practice")
IMAGE_PATH = PROJECT_ROOT / "images" / "clean.png"
ENV_FILE = PROJECT_ROOT / ".env"

# Ollama 模型配置
TEXT_MODEL = "qwen3.5"        # 文本对话模型
VISION_MODEL = "qwen3.5"  # 多模态模型

# ==================== 初始化 ====================

console = Console()
load_dotenv(dotenv_path=ENV_FILE)

def print_header():
    """打印头部信息"""
    console.print(Panel.fit(
        "[bold cyan]🤖 Ollama Cloud 多模态 AI 助手[/bold cyan]\n"
        "[dim]支持文本对话 + 图片理解 | Rich 美化输出[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    ))
    console.print()

def print_model_info():
    """显示模型信息表格"""
    table = Table(title="📋 模型配置", box=box.ROUNDED, border_style="green")
    table.add_column("项目", style="cyan", no_wrap=True)
    table.add_column("配置", style="white")
    
    table.add_row("文本模型", TEXT_MODEL)
    table.add_row("多模态模型", VISION_MODEL)
    table.add_row("图片路径", str(IMAGE_PATH))
    table.add_row("图片状态", "✅ 存在" if IMAGE_PATH.exists() else "❌ 不存在")
    
    console.print(table)
    console.print()

def check_api_key():
    """检查 API Key 配置"""
    api_key = os.getenv("OLLAMA_API_KEY")
    
    if not api_key:
        console.print(Panel(
            "[bold red]❌ 错误：未找到 OLLAMA_API_KEY[/bold red]\n"
            f"请在 [yellow]{ENV_FILE}[/yellow] 文件中配置 API Key\n"
            "格式：OLLAMA_API_KEY=your_key_here",
            title="配置错误",
            border_style="red"
        ))
        sys.exit(1)
    
    console.print(Panel(
        "[bold green]✅ API Key 配置成功[/bold green]",
        title="认证状态",
        border_style="green"
    ))
    console.print()
    
    return api_key

def get_client(api_key):
    """创建 Ollama 客户端"""
    return Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {api_key}"}
    )

def encode_image(image_path):
    """将图片编码为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def chat_text(client, message):
    """文本对话"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]正在思考中...[/bold blue]"),
        console=console,
    ) as progress:
        progress.add_task("", total=None)
        
        try:
            response = client.chat(
                model=TEXT_MODEL,
                messages=[{'role': 'user', 'content': message}]
            )
            return response['message']['content']
        except Exception as e:
            return f"[red]❌ 请求失败：{str(e)}[/red]"

def chat_vision(client, image_path, prompt="请描述这张图片"):
    """多模态图片理解"""
    if not image_path.exists():
        return f"[red]❌ 图片文件不存在：{image_path}[/red]"
    
    # 获取图片信息
    image_size = image_path.stat().st_size / 1024  # KB
    console.print(f"[dim]📷 图片大小：{image_size:.2f} KB[/dim]")
    
    # 编码图片
    image_base64 = encode_image(image_path)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold magenta]正在分析图片...[/bold magenta]"),
        console=console,
    ) as progress:
        progress.add_task("", total=None)
        
        try:
            response = client.chat(
                model=VISION_MODEL,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_base64]
                }]
            )
            return response['message']['content']
        except Exception as e:
            return f"[red]❌ 请求失败：{str(e)}[/red]"

def main():
    """主函数"""
    console.clear()
    print_header()
    
    # 检查 API Key
    api_key = check_api_key()
    
    # 显示模型信息
    print_model_info()
    
    # 创建客户端
    client = get_client(api_key)
    
    # ==================== 测试 1: 文本对话 ====================
    console.print(Panel(
        "[bold yellow]📝 测试 1: 文本对话[/bold yellow]",
        border_style="yellow"
    ))
    
    user_message = Prompt.ask(
        "[cyan]💬 请输入问题[/cyan]",
        default="你好，请介绍一下你自己"
    )
    
    response = chat_text(client, user_message)
    console.print(Panel(
        Markdown(response),
        title="🤖 AI 回答",
        border_style="green"
    ))
    console.print()
    
    # ==================== 测试 2: 多模态图片理解 ====================
    console.print(Panel(
        "[bold magenta]🖼️ 测试 2: 多模态图片理解[/bold magenta]",
        border_style="magenta"
    ))
    
    if IMAGE_PATH.exists():
        console.print(f"[green]✅ 找到图片：{IMAGE_PATH}[/green]")
        
        vision_prompt = Prompt.ask(
            "[cyan]💬 请输入图片分析问题[/cyan]",
            default="请详细描述这张图片的内容"
        )
        
        response = chat_vision(client, IMAGE_PATH, vision_prompt)
        console.print(Panel(
            Markdown(response),
            title="🤖 AI 图片分析",
            border_style="magenta"
        ))
    else:
        console.print(Panel(
            f"[red]❌ 图片不存在：{IMAGE_PATH}[/red]\n"
            f"请确保图片放在正确位置",
            border_style="red"
        ))
    
    console.print()
    console.print(Panel(
        "[bold cyan]✅ 测试完成！[/bold cyan]",
        border_style="cyan"
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 用户中断，已退出[/yellow]")
    except Exception as e:
        console.print(f"[bold red]❌ 程序错误：{e}[/bold red]")
        sys.exit(1)
