import os
import json
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

def run_agent(user_input):
    messages = [
        {
            "role": "user",
            "content": user_input
        }
    ]

    max_steps = 5
    step = 0
    while step < max_steps:
        step += 1
        print("\n==== 当前轮次：", step, "====")

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)
            # 遍历所有工具调用
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

                # ✅ 移到for循环内部，每处理完一个tool_call立刻追加消息
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            # for循环结束，本轮所有工具执行完毕，进入下一轮while循环
        else:
            # 模型不再调用工具，输出最终回答，退出循环
            return message.content


    return "已达到最大调用轮次，任务可能尚未完成"



answer = run_agent("先计算 20 加 30，再把结果乘以 2")
print(answer)