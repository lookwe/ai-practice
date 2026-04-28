"""
个人 RAG 知识库 - 智能客服脚本
基于 ChromaDB 实现向量检索，使用 Ollama 大模型进行智能问答
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
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
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"
ENV_FILE = PROJECT_ROOT / ".env"

# Ollama 模型配置
TEXT_MODEL = "qwen3.5"  # 文本对话模型

# ChromaDB 配置
COLLECTION_NAME = "knowledge_base"

# ==================== 初始化 ====================

console = Console()
load_dotenv(dotenv_path=ENV_FILE)


class RAGKnowledgeBase:
    """RAG 知识库管理类"""
    
    def __init__(self):
        """初始化知识库"""
        self.chroma_client = None
        self.collection = None
        self.ollama_client = None
        self._init_chromadb()
        self._init_ollama()
    
    def _init_chromadb(self):
        """初始化 ChromaDB"""
        console.print("[dim]📚 正在初始化 ChromaDB...[/dim]")
        
        # 创建持久化客户端
        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 获取或创建集合
        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
        )
        
        console.print("[dim]✅ ChromaDB 初始化完成[/dim]")
    
    def _init_ollama(self):
        """初始化 Ollama 客户端"""
        api_key = os.getenv("OLLAMA_API_KEY")
        
        if not api_key:
            console.print(Panel(
                "[bold yellow]⚠️ 警告：未找到 OLLAMA_API_KEY[/bold yellow]\n"
                f"请在 [yellow]{ENV_FILE}[/yellow] 文件中配置 API Key\n"
                "格式：OLLAMA_API_KEY=your_key_here",
                title="配置提示",
                border_style="yellow"
            ))
        
        self.ollama_client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {}
        )
        console.print("[dim]✅ Ollama 客户端初始化完成[/dim]")
    
    def load_documents(self, doc_dir: Optional[Path] = None):
        """加载文档到知识库
        
        Args:
            doc_dir: 文档目录路径，默认为配置的 DATA_DIR
        """
        if doc_dir is None:
            doc_dir = DATA_DIR
        
        if not doc_dir.exists():
            console.print(f"[red]❌ 文档目录不存在：{doc_dir}[/red]")
            return
        
        # 获取所有 .md 文件
        md_files = list(doc_dir.glob("*.md"))
        
        if not md_files:
            console.print(f"[yellow]⚠️ 未找到任何 .md 文件：{doc_dir}[/yellow]")
            return
        
        console.print(f"\n[bold cyan]📄 发现 {len(md_files)} 个文档[/bold cyan]")
        
        documents = []
        metadatas = []
        ids = []
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 分割文档为段落（按空行分割）
                paragraphs = self._split_document(content)
                
                for i, paragraph in enumerate(paragraphs):
                    if len(paragraph.strip()) < 20:  # 跳过太短的段落
                        continue
                    
                    documents.append(paragraph)
                    metadatas.append({
                        "source": file_path.name,
                        "paragraph_index": i
                    })
                    ids.append(f"{file_path.stem}_{i}")
                
            except Exception as e:
                console.print(f"[red]❌ 读取文件失败 {file_path.name}: {e}[/red]")
        
        if not documents:
            console.print("[yellow]⚠️ 没有有效的文档内容可添加[/yellow]")
            return
        
        # 添加到 ChromaDB
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]正在向量化文档...[/bold green]"),
            console=console,
        ) as progress:
            progress.add_task("", total=None)
            
            # 批量添加（避免单次过多）
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i+batch_size]
                batch_metas = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                
                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )
        
        console.print(f"\n[bold green]✅ 成功加载 {len(documents)} 个文档片段[/bold green]")
        console.print(f"[dim]知识库总数：{self.collection.count()} 个片段[/dim]")
    
    def _split_document(self, content: str, max_length: int = 500) -> List[str]:
        """将文档分割成适合向量的段落
        
        Args:
            content: 文档内容
            max_length: 每个段落的最大长度
            
        Returns:
            段落列表
        """
        # 首先按空行分割
        paragraphs = content.split('\n\n')
        result = []
        
        current_paragraph = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 如果当前段落 + 新段落超过限制，保存当前段落并开始新的
            if len(current_paragraph) + len(para) > max_length and current_paragraph:
                result.append(current_paragraph)
                current_paragraph = para
            else:
                if current_paragraph:
                    current_paragraph += "\n\n" + para
                else:
                    current_paragraph = para
        
        # 添加最后一个段落
        if current_paragraph:
            result.append(current_paragraph)
        
        return result
    
    def query(self, question: str, top_k: int = 3) -> List[dict]:
        """查询相关知识
        
        Args:
            question: 用户问题
            top_k: 返回的最相关结果数量
            
        Returns:
            相关文档片段列表
        """
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        
        # 整理结果
        relevant_docs = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                relevant_docs.append({
                    'content': doc,
                    'source': results['metadatas'][0][i]['source'] if results['metadatas'] else 'unknown',
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return relevant_docs
    
    def generate_answer(self, question: str, context: str) -> str:
        """使用大模型生成回答
        
        Args:
            question: 用户问题
            context: 相关上下文信息
            
        Returns:
            AI 生成的回答
        """
        # 构建提示词
        prompt = f"""你是一名专业的智能客服助手。请根据以下参考信息，用友好、专业的语气回答用户的问题。

## 参考信息：
{context}

## 用户问题：
{question}

## 回答要求：
1. 基于参考信息回答问题，不要编造信息
2. 如果参考信息不足以回答问题，请诚实告知用户
3. 回答要简洁明了，重点突出
4. 保持友好、专业的服务态度

请开始回答："""

        try:
            response = self.ollama_client.chat(
                model=TEXT_MODEL,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"[red]❌ 请求失败：{str(e)}[/red]"
    
    def chat(self, question: str, top_k: int = 3) -> str:
        """完整的 RAG 问答流程
        
        Args:
            question: 用户问题
            top_k: 检索的相关文档数量
            
        Returns:
            AI 回答
        """
        # 1. 检索相关知识
        relevant_docs = self.query(question, top_k)
        
        if not relevant_docs:
            return "抱歉，我暂时没有找到相关的信息来回答您的问题。您可以尝试换一种问法，或者联系人工客服获取帮助。"
        
        # 2. 构建上下文
        context = "\n\n".join([f"[来自 {doc['source']}]\n{doc['content']}" for doc in relevant_docs])
        
        # 3. 生成回答
        answer = self.generate_answer(question, context)
        
        return answer
    
    def get_stats(self) -> dict:
        """获取知识库统计信息"""
        return {
            'total_documents': self.collection.count(),
            'collection_name': COLLECTION_NAME
        }


def print_header():
    """打印头部信息"""
    console.print(Panel.fit(
        "[bold cyan]🤖 个人 RAG 知识库 - 智能客服系统[/bold cyan]\\n"
        "[dim]基于 ChromaDB + Ollama | 支持文档检索与智能问答[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    ))
    console.print()


def print_kb_stats(kb: RAGKnowledgeBase):
    """显示知识库统计信息"""
    stats = kb.get_stats()
    
    table = Table(title="📊 知识库状态", box=box.ROUNDED, border_style="green")
    table.add_column("项目", style="cyan", no_wrap=True)
    table.add_column("数值", style="white")
    
    table.add_row("集合名称", stats['collection_name'])
    table.add_row("文档片段总数", str(stats['total_documents']))
    
    console.print(table)
    console.print()


def main():
    """主函数"""
    console.clear()
    print_header()
    
    # 初始化知识库
    kb = RAGKnowledgeBase()
    
    # 检查是否需要加载文档
    if kb.collection.count() == 0:
        console.print(Panel(
            "[bold yellow]📚 检测到空知识库，正在加载文档...[/bold yellow]",
            border_style="yellow"
        ))
        kb.load_documents()
        console.print()
    
    # 显示知识库状态
    print_kb_stats(kb)
    
    # 主对话循环
    console.print(Panel(
        "[bold green]💬 进入对话模式 | 输入 'quit' 或 'exit' 退出[/bold green]",
        border_style="green"
    ))
    console.print()
    
    while True:
        try:
            # 获取用户输入
            user_input = Prompt.ask(
                "[cyan]👤 您[/cyan]",
                default=""
            ).strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("\n[yellow]👋 感谢使用，再见！[/yellow]")
                break
            
            # 处理命令
            if user_input.lower() == 'reload':
                console.print("\n[yellow]🔄 重新加载文档...[/yellow]\n")
                kb.load_documents()
                print_kb_stats(kb)
                continue
            
            if user_input.lower() == 'stats':
                print_kb_stats(kb)
                continue
            
            # RAG 问答
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]正在思考中...[/bold blue]"),
                console=console,
            ) as progress:
                progress.add_task("", total=None)
                answer = kb.chat(user_input)
            
            # 显示回答
            console.print(Panel(
                Markdown(answer),
                title="🤖 智能客服",
                border_style="blue"
            ))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 用户中断，已退出[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ 程序错误：{e}[/bold red]")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[bold red]❌ 程序启动失败：{e}[/bold red]")
        sys.exit(1)
