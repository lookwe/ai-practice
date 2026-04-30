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
| `chat_multimode.py` | Ollama Cloud API 多模态对话 | 文本对话 + 图片理解，支持 Rich 美化输出 |
| `rag_chatbot.py` | 个人 RAG 知识库智能客服系统 | 基于企业文档的智能问答客服 |
| `weather_assistant/` | AI 智能旅行助手 | 查询城市天气并推荐热门景点 |

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

### chat_multimode.py - Ollama Cloud API 多模态对话

这是一个基于 Ollama Cloud API 的多模态 AI 助手，具有以下特性：
- 支持文本对话和多模态图片理解
- 使用 Rich 库美化命令行输出
- 自动显示模型配置信息表格
- 支持自定义图片路径和对话问题
- 需要自行申请 Ollama API Key 并配置到 `.env` 文件

**功能亮点**：
- 🤖 文本对话：使用 `qwen3.5` 模型进行智能问答
- 🖼️ 图片理解：上传本地图片，AI 自动分析描述
- 🎨 Rich 美化：彩色面板、进度条、Markdown 格式化输出
- ⚙️ 灵活配置：可自定义模型、图片路径和 API Key

**环境配置**：
1. 在 `.env` 文件中配置 API Key：
```
OLLAMA_API_KEY=your_api_key_here
```

2. 确保图片文件存在于指定路径（默认：`images/clean.png`）

**快速开始**：
```bash
uv run python chat_multimode.py
```

### rag_chatbot.py - 个人 RAG 知识库智能客服系统

这是一个基于 RAG（检索增强生成）技术的智能客服系统，具有以下特性：
- 📚 **RAG 知识库**：基于 ChromaDB 向量数据库实现文档检索
- 🤖 **智能问答**：使用 Ollama 大模型生成专业回答
- 📄 **文档自动加载**：自动扫描 `data/` 目录下的 Markdown 文件构建知识库
- 🔍 **语义检索**：通过向量相似度搜索最相关的文档片段
- ⏱️ **超时保护**：内置 2 分钟超时机制，避免长时间等待
- 🎨 **Rich 美化界面**：彩色命令行界面，实时显示处理进度

**核心功能**：
- **文档管理**：支持自动加载、重新加载 (`reload` 命令) 和状态查看 (`stats` 命令)
- **智能分割**：自动将文档按段落分割并控制长度（最大 500 字符）
- **上下文构建**：检索 Top-K 相关文档片段，构建回答上下文
- **专业回答**：基于参考信息生成友好、专业的客服回答，不编造信息

**数据目录结构**：
```
data/
├── company_info.md      # 公司信息
├── faq.md              # 常见问题解答
├── product_service.md  # 产品服务说明
├── tech_support.md     # 技术支持文档
└── terms_of_service.md # 服务条款
```

**命令说明**：
- 直接输入问题：进行智能问答
- `reload`：重新加载文档到知识库
- `stats`：查看知识库统计信息（文档片段总数等）
- `quit` / `exit` / `q`：退出程序

**环境配置**：
1. 在 `.env` 文件中配置必要的 API Key：
```
OLLAMA_API_KEY=your_ollama_api_key
MODEL_NAME=qwen3.5
```

2. 确保 `data/` 目录下有相关的业务文档（Markdown 格式）

**快速开始**：
```bash
uv run python rag_chatbot.py
```

**运行示例**：
```
🤖 个人 RAG 知识库 - 智能客服系统
基于 ChromaDB + Ollama | 支持文档检索与智能问答

📊 知识库状态
┌──────────────┬─────────────┐
│ 项目         │ 数值        │
├──────────────┼─────────────┤
│ 集合名称     │ knowledge_  │
│              │ base        │
│ 文档片段总数 │ 45          │
└──────────────┴─────────────┘

💬 进入对话模式 | 输入 'quit' 或 'exit' 退出

👤 您：你们公司的退货政策是什么？
正在思考中...

┌─────────────────────────────────────┐
│ 🤖 智能客服                         │
├─────────────────────────────────────┤
│ 根据我们的服务条款，产品购买后 7    │
│ 天内可以申请无理由退货...           │
└─────────────────────────────────────┘
```

### weather_assistant/ - AI 智能旅行助手

这是一个基于 Agent 架构的智能旅行推荐助手，具有以下特性：
- 🤖 **Agent 自主决策**：通过 Thought-Action 循环自主规划任务执行流程
- 🌤️ **天气查询**：自动调用工具查询城市实时天气信息
- 🏛️ **景点推荐**：根据城市和天气情况智能推荐热门旅游景点
- 🎨 **Rich 美化输出**：彩色命令行界面，清晰展示思考过程和 execution 结果
- ⚙️ **灵活配置**：支持自定义 Ollama 模型、API Key 和系统提示词

**功能亮点**：
- 🔄 **智能循环**：自动执行"思考→行动→观察"循环，最多 10 次迭代
- 🛠️ **工具集成**：内置 `get_weather` 和 `get_attraction` 两个工具函数
- 📝 **过程可视化**：实时显示 Agent 的 Thought 和 Action 执行过程
- 🌍 **多城市支持**：可查询任意城市的天气和景点推荐

**环境配置**：
1. 在 `.env` 文件中配置必要的 API Key：
```
TAVILY_API_KEY=your_tavily_api_key
OLLAMA_API_KEY=your_ollama_api_key
AGENT_SYSTEM_PROMPT=你的系统提示词
MODEL_NAME=qwen3.5
OLLAMA_BASE_URL=https://ollama.com/v1
```

2. 确保 `weather_assistant/tools.py`、`weather_assistant/weather.py`、`weather_assistant/attractions.py` 文件存在

**快速开始**：
```bash
uv run python weather_assistant/main.py
```

**运行示例**：
```
=== 智能旅行助手 ===
请输入城市名称：北京

正在查询 北京的天气和景点推荐...

Thought: 我需要先查询北京的天气情况
Action: get_weather(city="北京")
天气查询结果：晴朗，温度 25°C

Thought: 根据天气情况推荐适合的景点
Action: get_attraction(city="北京", weather="晴朗")
景点搜索结果：共 5 条

=== 推荐结果 ===
[AI 生成的详细景点推荐内容]
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
