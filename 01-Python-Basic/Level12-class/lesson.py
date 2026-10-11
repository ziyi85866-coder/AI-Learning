# class ChatBot:

#     def hello(self):
#         print("你好，我是AI机器人")
# bot = ChatBot()

# bot.hello()
#第一版
# class ChatBot:

#     def __init__(self):
#         print("机器人创建成功！")

# bot = ChatBot()
#第二版
# class ChatBot:

#     def __init__(self):
#         self.name = "小智"

#     def hello(self):
#         print(f"你好，我是{self.name}")

# bot = ChatBot()

# bot.hello()

class ChatBot:

    def __init__(self):
        self.name = "小智"
        self.messages = []

    def hello(self):
        print(f"你好，我是{self.name}")

bot = ChatBot()

bot.hello()

print(bot.messages)