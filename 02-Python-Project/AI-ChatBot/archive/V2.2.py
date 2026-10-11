from dotenv import load_dotenv
from openai import OpenAI
import os
import json

class ChatBot:

    def __init__(self):

        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3"
        )
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
                model="deepseek-v4-1-flash-260910",
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
                    "content": "你是一名Python老师，请一步一步回答问题。"
                }
            ]

    def save_messages(self):
        with open("messages.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(
                self.messages,
                ensure_ascii=False
            )
            )

    def clear_messages(self):
        self.messages = [
            {
                "role": "system",
                "content": "你是一名Python老师，请一步一步回答问题。"
            }
        ]
        self.save_messages()
        print("聊天记录已清空！")
    def show_history(self):
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
        if user_input == "exit":
             return False
        if user_input == "/clear":
             self.clear_messages()
             return True
        if user_input == "/history":
             self.show_history()
             return True
        return False

bot = ChatBot()
while bot.chat():  # ChatBot.chat(bot)
    pass
print("程序结束")