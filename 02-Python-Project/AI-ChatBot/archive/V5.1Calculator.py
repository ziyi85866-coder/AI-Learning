from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import datetime


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

class ChatBot:

    def __init__(self):

        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3"
        )
        self.model = "deepseek-v4-1-flash-260910"
        self.system_prompt ="你是一名Python老师，请一步一步回答问题。"
        self.commands = {
            "/help": self.show_help,
            "/history": self.show_history,
            "/clear": self.clear_messages,
            "/model": self.show_model,
            "/time": self.show_time,
            "/calc": self.show_calc,
        }
        self.messages = self.load_messages()

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
            self.save_messages()
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
                stream=True
            )

            # answer = response.choices[0].message.content
            answer = ""
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    answer += content

            print()
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
            return  [
                {
                    "role": "system",
                    "content": self.system_prompt
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

    def show_time(self,argument=""):
        now = datetime.datetime.now()

        print("当前时间：",now.strftime("%Y-%m-%d %H:%M:%S"))
    def show_calc(self,argument=""):
        result = eval(argument)
        print(f"结果：{result}")

bot = ChatBot()
while bot.chat():  # ChatBot.chat(bot)
    pass
print("程序结束")