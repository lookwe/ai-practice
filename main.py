# 1. 导入库 (类似 JS 的 import/require)
import os               # 操作系统接口，用于读取环境变量
from dotenv import load_dotenv # 加载 .env 文件
from rich.console import Console   # 用于打印漂亮的彩色输出
from rich.markdown import Markdown # 用于渲染 Markdown 格式的回答
import ollama           # 调用本地 Ollama 模型的库

# 初始化富文本控制台 (类似 new Console())
console = Console()

# 2. 加载环境变量
# JS: require('dotenv').config()
load_dotenv() 

# 3. 获取配置变量
# JS: const modelName = process.env.MODEL_NAME;
# Python: 不需要 var/let，直接赋值。如果变量不存在，os.getenv 返回 None (类似 null)
model_name = os.getenv("MODEL_NAME", "qwen2.5-coder:7b") 
system_role = os.getenv("SYSTEM_ROLE", "你是一个助手。")

# 4. 定义函数 (类似 JS function 或 Java method)
# 语法重点：
# - 使用 def 关键字
# - 参数后加冒号 :
# - 函数体必须缩进 (通常是 4 个空格)
# - 不需要大括号 {}
def ask_ai(user_question: str):
    """
    向本地 AI 发送问题并获取回答
    :param user_question: 用户的问题字符串
    """
    
    # 构建消息列表 (类似 JS 的对象数组)
    # Python 列表用 []，字典(对象)用 {}
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_question}
    ]

    console.print(f"\n[bold blue]🤔 思考中... (模型: {model_name})[/bold blue]")

    try:
        # 调用 Ollama API
        # stream=False 表示一次性返回所有结果 (类似 await fetch)
        response = ollama.chat(model=model_name, messages=messages)
        
        # 提取回答内容
        # JS: response.message.content
        # Python: response['message']['content'] (字典取值用方括号或 .get())
        answer = response['message']['content']

        # 打印结果
        # Rich 库可以自动渲染 Markdown，让代码高亮显示
        console.print("\n[bold green]✅ AI 回答:[/bold green]")
        console.print(Markdown(answer))

        # 保存到文件（修正版）
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_response_{timestamp}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(answer)

        console.print(f"[dim]💾 已保存到 {filename}[/dim]")

    except Exception as e:
        # 异常处理 (类似 JS try...catch 或 Java try...catch)
        # f-string: 在字符串前加 f，可以用 {变量名} 直接插值 (类似 JS 模板字符串 `${var}`)
        console.print(f"[bold red]❌ 出错了: {e}[/bold red]")
        console.print("提示：请确保 Ollama 正在运行，且模型已下载。")

# 5. 程序入口
# JS: if (require.main === module) { ... }
# Java: public static void main(String[] args)
# Python: 当直接运行此文件时，__name__ 等于 "__main__"
if __name__ == "__main__":
    console.print("[bold yellow]👋 欢迎使用本地 AI 编程助手![/bold yellow]")
    console.print("输入 'quit' 退出。\n")

    # while 循环 (类似 JS while)
    while True:
        # input() 获取用户输入 (类似 readline 或 prompt)
        # 注意：input 返回的永远是字符串
        user_input = input("👉 请输入你的问题: ")

        # 条件判断 (类似 JS if)
        # 注意：Python 不需要括号 () 包裹条件，但必须有冒号 :
        if user_input.lower() in ["quit", "exit", "q"]:
            console.print("[dim]再见！👋[/dim]")
            break # 跳出循环 (类似 JS break)
        
        # 跳过空输入
        if not user_input.strip():
            continue # 跳过本次循环 (类似 JS continue)

        # 调用函数
        ask_ai(user_input)
