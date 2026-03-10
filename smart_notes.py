# 1. 导入必要的库
import os               # JS: import fs from 'fs'; (用于文件和目录操作)
from pathlib import Path # JS: import path from 'path'; (更现代的路径处理工具)
from ollama import chat
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime

# 初始化控制台
console = Console()

# 2. 配置工作目录
# JS: const notesDir = './notes'; if (!fs.existsSync(notesDir)) fs.mkdirSync(notesDir);
notes_dir = Path("notes")
# exists_ok=True 意思是：如果文件夹已存在就不报错，没有就创建
notes_dir.mkdir(exist_ok=True)

console.print("[bold cyan]📒 AI 智能笔记整理助手[/bold cyan]")
console.print("[dim]输入杂乱的笔记，AI 将为你整理成结构化 Markdown 文件。输入 'q' 退出。[/dim]\n")

# 3. 定义系统提示词 (Prompt Engineering)
# 这里的关键是要求 AI 输出特定的 Markdown 格式
system_instruction = """
你是一个专业的笔记整理专家。
用户会输入一段杂乱的文本（可能是会议记录、灵感、待办事项）。
请你执行以下操作：
1. 提炼一个简洁的标题 (Title)。
2. 将内容整理为结构清晰的 Markdown 格式：
   - 使用 ## 标题
   - 使用 - 列表项
   - 如果有待办事项，使用 [ ] 已经完成的 [x] 标记
   - 如果有代码，放入代码块
3. **不要**输出任何开场白（如“好的，这是整理后的...”），直接输出 Markdown 内容。
4. 在输出的最第一行，用 HTML 注释写上建议的文件名，格式：<!-- filename: my-note-title.md -->
"""

messages = [
    {"role": "system", "content": system_instruction}
]

while True:
    # --- 步骤 A: 获取用户输入的杂乱笔记 ---
    user_input = Prompt.ask("\n[bold yellow]📝 输入笔记内容[/bold yellow]")

    if user_input.lower() in ["quit", "exit", "q"]:
        console.print("[dim]👋 笔记整理完毕，再见！[/dim]")
        break

    if not user_input.strip():
        continue

    # 将用户输入加入上下文
    messages.append({"role": "user", "content": user_input})

    console.print("[dim]✨ 正在整理笔记...[/dim]")

    try:
        # --- 步骤 B: 调用 AI ---
        response = chat(
            model='qwen3-coder:480b-cloud',
            messages=messages
        )
        
        ai_content = response['message']['content']

        # --- 步骤 C: 解析 AI 的返回结果 ---
        
        # 1. 提取建议的文件名
        # 我们约定 AI 在第一行写 <!-- filename: xxx.md -->
        # JS 类比: const match = aiContent.match(/<!-- filename: (.*?) -->/);
        import re
        filename_match = re.search(r"<!--\s*filename:\s*(.*?)\s*-->", ai_content)
        
        if filename_match:
            suggested_filename = filename_match.group(1).strip()
            # 清理文件名中的非法字符 (简单处理)
            safe_filename = "".join(c for c in suggested_filename if c.isalnum() or c in "._- ")
            if not safe_filename.endswith('.md'):
                safe_filename += '.md'
        else:
            # 如果 AI 没遵守规则，给个默认名
            safe_filename = f"note_{datetime.now().strftime('%H%M%S')}.md"
            console.print("[dim]⚠️ 未检测到建议文件名，使用默认名称。[/dim]")

        # 2. 清理内容 (去掉那行文件名注释，只保留纯 Markdown)
        # JS 类比: cleanContent = aiContent.replace(match[0], '').trim();
        clean_content = re.sub(r"<!--\s*filename:.*?-->\n?", "", ai_content).strip()

        # --- 步骤 D: 保存文件 ---
        file_path = notes_dir / safe_filename  # JS: path.join(notesDir, safeFilename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {safe_filename[:-3]}\n\n") # 额外加个大标题
            f.write(clean_content)

        # --- 步骤 E: 反馈给用户 ---
        console.print(f"\n[bold green]✅ 笔记已保存:[/bold green] [underline]{file_path}[/underline]")
        console.print("\n[bold]预览:[/bold]")
        # 只显示前 500 个字符的预览，避免刷屏
        preview = clean_content[:500] + ("..." if len(clean_content) > 500 else "")
        console.print(Markdown(preview))

        # 清空上下文，因为每次笔记整理是独立的任务 (不像聊天那样需要连续记忆)
        # 如果想连续修改同一篇笔记，可以注释掉下面这行
        messages = [{"role": "system", "content": system_instruction}]

    except Exception as e:
        console.print(f"[bold red]❌ 整理失败:[/bold red] {e}")
        # 出错时保留上下文，方便调试，或者选择重置
        messages = [{"role": "system", "content": system_instruction}]
