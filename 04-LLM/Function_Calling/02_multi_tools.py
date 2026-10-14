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


tools = [
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "计算两个数字的差",
            "parameters": {
                "type": "object",
                "properties": {
                       "a": {"type": "number"},
                        "b": {"type": "number"}
               },
               "required": ["a", "b"]
           }
       }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字的和",
            "parameters": {
                "type": "object",
                "properties": {
                       "a": {"type": "number"},
                        "b": {"type": "number"}
               },
               "required": ["a", "b"]
           }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "计算两个数字的积",
            "parameters": {
                "type": "object",
                "properties": {
                       "a": {"type": "number"},
                        "b": {"type": "number"}
               },
               "required": ["a", "b"]
           }
        }
    },
]
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b


# 1. 创建工具映射字典
tool_functions = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply
}


messages = [
    {
        "role": "user",
        "content": "请分别计算 12 乘以 8，以及 100 减去 35，两个计算都要使用工具。"
    }
]

response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools
)

message = response.choices[0].message

import json

if message.tool_calls:
    messages.append(message)
    for tool_call in message.tool_calls:
        result = None
        tool_name = tool_call.function.name
        arguments_text = tool_call.function.arguments

        print("工具名称：", tool_call.function.name)
        print("工具参数：", tool_call.function.arguments)


        if tool_name not in tool_functions:
            result = "错误：工具不存在"
            print(result)

        else:
            try:
                arguments = json.loads(arguments_text)

                if not isinstance(arguments, dict):
                    result = "错误：参数必须是 JSON 对象"
                    print(result)
                elif "a" not in arguments or "b" not in arguments:
                    result = "错误：缺少必要参数"
                    print(result)

                elif (
                       type(arguments["a"]) not in (int, float)
                        or type(arguments["b"]) not in (int, float)
                   ):
                    result = "错误：参数必须是数字"
                    print(result)

                else:
                    func = tool_functions[tool_name]
                    result = func(arguments["a"], arguments["b"])
                    print("工具执行结果：", result)

            except json.JSONDecodeError:
                result = "错误：JSON 格式不正确"
                print(result)
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
else:
    print("模型没有请求调用工具")