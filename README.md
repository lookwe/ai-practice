# AI编程助手

基于本地Ollama模型的AI编程助手，使用Python和Rich库构建的命令行工具。

## 功能特性

- 🤖 支持本地Ollama模型
- 📝 丰富的Markdown格式输出
- 💾 自动保存AI响应到文件
- 🎨 彩色命令行界面
- ⚙️ 可配置模型和系统角色

## 脚本目录

| 脚本名称 | 功能描述 | 适用场景 |
|---------|---------|---------|
| `main.py` | 基础一问一答对话 | 简单问答，无需记忆上下文 |
| `chat_history.py` | 多轮记忆对话 | 连续对话，需要记住历史上下文 |
| `smart_notes.py` | 会议记录文章灵魂自动笔记生成 | 开会的内容和临时的想法和计划 |
| `bubble_sort.py` | 冒泡排序算法实现 | 学习排序算法、算法演示 |

### main.py - 基础一问一答

这是一个简单的命令行AI对话工具，支持：
- 独立问答模式，每次对话都是全新的
- 自动保存AI响应到文件（带时间戳）
- 丰富的Markdown格式输出
- 可配置模型和系统角色

**快速开始**：
```bash
uv run python main.py
```

### chat_history.py - 多轮记忆对话

这是一个支持上下文记忆的对话工具，具有以下特性：
- 完整的对话历史记忆
- 连续多轮对话，AI能记住之前的交流
- 对话日志自动保存到 `chat_log.md`
- 系统预设为前端工程师专家人设

**快速开始**：
```bash
uv run python chat_history.py
```

### bubble_sort.py - 冒泡排序算法

这是一个经典的排序算法实现，具有以下特性：
- 标准的冒泡排序算法实现
- 包含优化版本（提前终止）
- 提供示例代码和测试数据
- 适合学习排序算法原理

**快速开始**：
```bash
uv run python bubble_sort.py
```

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
