# 1. 导入必要的库
# JS: import { ChatOllama } from 'langchain/ollama'; (假设用 langchain)
# 这里我们直接用原生 ollama 库，更轻量
from ollama import chat

# JS: import { Markdown, console, prompt } from 'rich'; (类比)
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt # 专门用于获取用户输入的增强版工具

# 初始化控制台对象，用于打印漂亮的内容
# JS: const console = new Console(); (rich 库需要实例化)
console = Console()

# 2. 初始化“记忆”列表
# 这是一个 Python 列表 (List)，用来存储对话历史
# JS: let messages = [];
messages = []

# 添加一个“系统提示词”，设定 AI 的人设
# 这就像你在 JS 数组里 unshift 第一个对象
# JS: messages.unshift({ role: 'system', content: '你是一个乐于助人的编程专家...' });
messages.append({
    "role": "system", 
    "content": "你是一个乐于助人的 前端工程师专家。请用简洁、清晰的中文回答，代码示例请包含注释。"
})

console.print("[bold green]🤖 AI 助手已就绪 (输入 'quit' 退出)[/bold green]")

# 3. 开始无限循环，直到用户想退出
# JS: while (true) { ... }
while True:
    # --- 步骤 A: 获取用户输入 ---
    # Prompt.ask 是 rich 库提供的，比 input() 更漂亮，支持默认值和颜色
    # JS: const userInput = prompt("你: "); 
    user_input = Prompt.ask("\n[bold blue]你[/bold blue]")

    # 检查退出条件
    # JS: if (userInput === 'quit' || userInput === 'exit') break;
    if user_input.lower() in ["quit", "exit", "q"]:
        console.print("[dim]👋 再见！祝编码愉快！[/dim]")
        break

    # 将用户的问题加入“记忆”列表
    # JS: messages.push({ role: 'user', content: userInput });
    messages.append({"role": "user", "content": user_input})

    # --- 步骤 B: 调用 AI (带上历史记录) ---
    console.print("[dim]🤔 AI 正在思考...[/dim]")
    
    try:
        # 调用 ollama.chat
        # 关键点：把整个 messages 列表传过去，AI 就能看到之前的对话了！
        # JS: const response = await ollama.chat({ model: 'qwen2.5', messages: messages });
        response = chat(
            model='qwen3-coder:480b-cloud',  # 确保你本地有这个模型，没有的话换成 'llama3' 或 'gemma2'
            messages=messages
        )

        # 提取 AI 的回答内容
        # JS: const aiContent = response.message.content;
        ai_content = response['message']['content']

        # --- 步骤 C: 显示并保存回答 ---
        
        # 1. 在终端漂亮地打印 Markdown 格式的回答
        # JS: console.log(new Markdown(aiContent));
        console.print("\n[bold green]✅ AI:[/bold green]")
        console.print(Markdown(ai_content))

        # 2. 把 AI 的回答也加入“记忆”列表 (这样下一轮它才知道自己说过什么)
        # JS: messages.push({ role: 'assistant', content: aiContent });
        messages.append({"role": "assistant", "content": ai_content})

        # 为了防止记忆过长，我们只保留最近的 20 条记录
        if len(messages) > 20:
            messages.pop(0) # 移除最旧的一条记录

        console.print(f"[dim]💾 当前记忆条数：{len(messages)}[/dim]")

        # 3. (可选) 自动保存到文件，记录这次对话
        # 我们简单地把最新一条记录追加到 log 文件
        # JS: fs.appendFileSync('chat_log.md', `...\n`);
        # 'a' 代表 append (追加模式)，不会覆盖旧内容
        # 'w' 代表 write (写入模式)，会覆盖旧内容
        with open("chat_file/chat_log.md", "a", encoding="utf-8") as f:
            f.write(f"\n---\n**User**: {user_input}\n\n**AI**:\n{ai_content}\n")

    except Exception as e:
        # 错误处理
        # JS: catch (error) { console.error(error); }
        console.print(f"[bold red]❌ 出错了:[/bold red] {e}")
        console.print("[dim]提示：请确保 Ollama 服务已启动 (ollama serve)，且模型已下载。[/dim]")
