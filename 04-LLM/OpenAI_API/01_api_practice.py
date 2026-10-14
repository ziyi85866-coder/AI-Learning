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
# 第一步：调用模型
response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": "请用一句话介绍 Python"}
    ]
)

# 第二步：获取并打印回答
answer = response.choices[0].message.content
print(answer)