from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

print("当前读取到的 Key:", os.getenv('MODELSCOPE_API_KEY'))

client = OpenAI(
    api_key=os.getenv('MODELSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", # 就是这个打不开的地址
)

response = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)
