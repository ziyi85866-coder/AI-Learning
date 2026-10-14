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
messages=[
        {
         "role": "system",
         "content": "你现在是一名Python入门老师，用通俗易懂的语言回答问题，回答包含“概念解释”和“代码示例”两部分。"
                    "同时满足概念解释不超过 100 个汉字；只能给出一个代码示例；示例代码不超过 8 行；不介绍字典的删除、遍历等进阶操作。"
         },
         {
        "role": "user",
        "content": "什么是 Python 字典？"
         }
    ]
# 第一步：调用模型
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
)

# 第二步：获取并打印回答
answer = response.choices[0].message.content
print(answer)