# AI编程助手

基于本地Ollama模型的AI编程助手，使用Python和Rich库构建的命令行工具。

## 功能特性

- 🤖 支持本地Ollama模型
- 📝 丰富的Markdown格式输出
- 💾 自动保存AI响应到文件
- 🎨 彩色命令行界面
- ⚙️ 可配置模型和系统角色

## 环境要求

- Python >= 3.13
- [Ollama](https://ollama.com/) 本地服务
- uv 包管理器

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/<your-username>/ai-practice.git
cd ai-practice
```

2. 安装依赖：
```bash
uv sync
```

3. 配置环境变量（可选）：
创建 `.env` 文件：
```
MODEL_NAME=qwen2.5-coder:7b
SYSTEM_ROLE=你是一个助手
```

## 使用方法

1. 启动Ollama服务：
```bash
ollama serve
```

2. 运行程序：
```bash
uv run python main.py
```

3. 交互式对话：
- 输入问题与AI对话
- 输入 `quit`、`exit` 或 `q` 退出程序

## 项目结构

```
ai-practice/
├── main.py              # 主程序文件
├── pyproject.toml       # 项目配置
├── README.md            # 项目说明
└── .gitignore          # Git忽略文件
```

## 依赖项

- ollama >= 0.6.1
- python-dotenv >= 1.2.2
- rich >= 14.3.3

## 注意事项

- 确保Ollama服务正在运行
- 确保所选模型已下载
- AI响应会自动保存为 `ai_response_<timestamp>.md` 文件

## License

MIT License