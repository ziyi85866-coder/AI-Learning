from dotenv import load_dotenv
from openai import OpenAI
import os
import json

import ast
import operator
from tools.calculator import Calculator
from tools.time_tool import TimeTool
from managers.conversation_manager import ConversationManager

# 帮助文本定义
help_text = """
=== 命令列表 ===
/clear    清空当前全部聊天记录
/history  查看完整对话历史
/help     显示本帮助信息
/model     查看当前模型
/time      查看当前时间
exit      退出程序
"""
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression"
                }
            },
            "required": ["expression"]
        }
    }
}
time_tool = {
    "type": "function",
    "function": {
        "name": "time",
        "description": "Get current local time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

class ChatBot:

    def __init__(self):

        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3"
        )
        self.calculator = Calculator()
        self.time_tool = TimeTool()
        self.model = "deepseek-v4-1-flash-260910"
        self.system_prompt = self.build_system_prompt(
            role="Python 和 Agent 开发老师",
            topic="Agent 开发",
            style="回答简洁，分步骤讲解，优先提供可运行代码。"
        )
        self.commands = {
            "/help": self.show_help,
            "/history": self.show_history,
            "/clear": self.clear_messages,
            "/model": self.show_model,
            "/time": self.show_time,
            "/calc": self.show_calc,
        }
        self.tools = []

        self.tool_dispatch = {}
        self.register_tool(calculator_tool, self.show_calc)

        self.register_tool(time_tool, self.show_time)

        self.conversation_manager = ConversationManager(
            self.system_prompt
        )

        self.messages = self.conversation_manager.load_messages()


        print("ChatBot 创建成功！")
    def chat(self):

        user_input = input("\n你：")
        if user_input == "exit":
            return False

        if self.handle_command(user_input):
            return True

        self.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
        answer = self.ask_ai()
        if answer:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )
            self.conversation_manager.save_messages(
                self.messages
            )
            print(f"\nAI：{answer}")
        else:
            self.messages.pop()
            print("请求失败，请稍后重试。")
            return True

        # print("\nAI：")
        # print(answer)
        return True

    def ask_ai(self):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                # stream=True
            )

            message = response.choices[0].message

            # 没有工具调用，直接返回文本
            if not message.tool_calls:
                return message.content

            self.messages.append(message.model_dump())

            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name

            arguments = json.loads(tool_call.function.arguments)

            # 执行计算

            tool = self.tool_dispatch[tool_name]
            if tool is None:
                return f"未知工具：{tool_name}"
            result = tool(**arguments)

            # 追加tool角色消息
            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )
            # 二次请求大模型，拿到最终回答
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            answer = response.choices[0].message.content

            return answer

        except Exception as e:
            print(f"请求 AI 失败：{e}")
            return ""

    def load_messages(self):
        try:
            with open("messages.json", "r", encoding="utf-8") as file:
                text = file.read()
                messages = json.loads(text)
                return messages
        except:
            return [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": "什么是 Python 列表？"
                },
                {
                    "role": "assistant",
                    "content": """📖 概念
            Python 列表（List）是一种有序、可修改的数据类型，用于保存多个元素。
            💻 示例
            ```python
            numbers = [1, 2, 3]
            print(numbers[0])
            ```
            ```text
            📝 总结
            ```
            """  # 你原来缺少结尾三引号！
                }
            ]
    def save_messages(self):
        with open("messages.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(
                self.messages,
                ensure_ascii=False
            )
            )

    def clear_messages(self,argument=""):
        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]
        self.save_messages()
        print("聊天记录已清空！")
    def show_history(self,argument=""):
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            if role == "system":
                print("系统：",content)

            elif role == "user":
                print("你：",content)

            elif role == "assistant":
                print("AI：",content)

    def handle_command(self, user_input):

        parts = user_input.split(maxsplit=1)
        command = parts[0]
        if len(parts) > 1:
             argument = parts[1]

        else:
            argument = ""
        if command in self.commands:
            self.commands[command](argument)
            return True
        return False

    def show_help(self,argument=""):
        print(help_text)

    def show_model(self,argument=""):
        # print("当前模型：",self.model)
        print(f"当前模型：{self.model}")

    def show_time(self, argument=""):
        return self.time_tool.run()

        return now.strftime("%Y-%m-%d %H:%M:%S")

    def show_calc(self, expression=""):
        try:
            result = self.calculator.run(expression)
            return str(result)
        except ValueError as e:
            return str(e)



    def register_tool(self, tool, func):
        self.tools.append(tool)

        tool_name = tool["function"]["name"]

        self.tool_dispatch[tool_name] = func

    def build_system_prompt(self, role, topic, style):
        with open(
                "prompts/system_prompt.txt",
                "r",
                encoding="utf-8"
        ) as f:
            template = f.read()

        return template.format(
            role=role,
            topic=topic,
            style=style
        )
            
bot = ChatBot()
while bot.chat():  # ChatBot.chat(bot)
    pass
print("程序结束")