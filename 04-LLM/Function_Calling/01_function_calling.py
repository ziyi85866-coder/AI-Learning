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

def subtract(a,b):
    return a-b
tools = [
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "计算两个数字的差",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number",
                          "description": "第一个数字"
                         },
                    "b": {"type": "number",
                         "description": "第二个数字"
                         }
                },
                "required": ["a", "b"]
            }
        }
    }
]
messages = [
    {
        "role": "user",
        "content": "请计算 100 减去 35"
    }
]

response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools
)

message = response.choices[0].message

print("模型返回的内容：", message.content)
print("模型请求调用的工具：", message.tool_calls)

import json

if message.tool_calls:
    tool_call = message.tool_calls[0]

    tool_name = tool_call.function.name
    arguments_text = tool_call.function.arguments

    # 1. 将 JSON 字符串转换为字典
    arguments = json.loads(arguments_text)

    # 2. 判断模型选择的工具
    if tool_name == "subtract":

        # 3. 从字典中获取 a、b
        a = arguments["a"]
        b = arguments["b"]

        # 4. 调用自己写的 subtract 函数
        result = subtract(a,b)

        print("工具执行结果：", result)
messages.append(message)

messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

final_response = client.chat.completions.create(
    model=model_name,
    messages=messages,
)

final_answer = final_response.choices[0].message.content

print("模型最终回答：", final_answer)