import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)
messages = [
    {
        "role": "system",
        "content": (
            "你是一名 Python 入门老师。"
            "请只返回 JSON 格式的数据，不要添加其他说明或 Markdown 代码块。"
            "JSON 必须包含三个字段：concept、example、difficulty。"
            "其中 difficulty 只能是简单、中等、困难之一。"
        )
    },
    {
        "role": "user",
        "content": "什么是 Python 列表？"
    }
]

# 第一步：调用模型
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    response_format={"type": "json_object"}
)

# 第二步：获取并打印回答
text = response.choices[0].message.content

# 1. 将 JSON 字符串转换成 Python 字典
try:
    data = json.loads(text)
    print(data["concept"])
    print(data["example"])
    print(data["difficulty"])
except json.JSONDecodeError:
    print("模型返回的内容不是合法 JSON")


