
import json
from openai import OpenAI

# 导入我们自己编写的工具类
from tools.calculator import Calculator
from tools.time_tool import TimeTool

# 导入各个管理类
from managers.conversation_manager import ConversationManager
from managers.prompt_manager import PromptManager
from config.config_manager import ConfigManager
from utils.logger import setup_logger


# ==================== 1. 命令帮助信息 ====================

# 三引号可以定义多行字符串，方便保存帮助文本
help_text = """
=== 命令列表 ===
/clear    清空当前全部聊天记录
/history  查看完整对话历史
/help     显示本帮助信息
/model    查看当前模型
/time     查看当前时间
/calc     计算数学表达式
exit      退出程序
"""


# ==================== 2. 定义 AI 可使用的工具 ====================

# 注意：下面的字典不是计算器的实现代码
# 它是提供给大模型的“工具说明书”
# 告诉模型：工具叫什么、能做什么、需要哪些参数

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

# 时间工具不需要输入参数，所以 properties 为空字典
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


# ==================== 3. ChatBot 主类 ====================

class ChatBot:

    def __init__(self):
        """
        构造方法：创建 ChatBot 对象时自动执行。

        主要完成：
        1. 读取配置
        2. 初始化大模型客户端
        3. 创建工具对象
        4. 加载系统提示词
        5. 注册命令和工具
        6. 加载聊天记录
        7. 初始化日志
        """

        # 创建配置管理对象
        # ConfigManager 负责从环境变量读取 API Key、模型名称等配置
        self.config = ConfigManager()

        # 创建 OpenAI 客户端
        # 这里使用兼容 OpenAI API 的模型服务
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

        # 保存当前使用的模型名称
        self.model = self.config.model

        # 创建工具实例
        # 后续通过 self.calculator.run() 执行计算
        self.calculator = Calculator()
        self.time_tool = TimeTool()

        # 创建提示词管理器
        self.prompt_manager = PromptManager()

        # 读取提示词模板，并替换其中的变量
        # 最终得到完整的 system prompt
        self.system_prompt = self.prompt_manager.build_prompt(
            "system_prompt.txt",
            role="Python 和 Agent 开发老师",
            topic="Agent 开发",
            style="回答简洁，分步骤讲解，优先提供可运行代码。"
        )

        # 命令映射字典
        # 键：用户输入的命令
        # 值：负责处理该命令的方法
        #
        # 注意：这里没有加括号
        # self.show_help 表示引用方法
        # self.show_help() 才表示立即执行方法
        self.commands = {
            "/help": self.show_help,
            "/history": self.show_history,
            "/clear": self.clear_messages,
            "/model": self.show_model,
            "/time": self.show_time,
            "/calc": self.show_calc,
        }

        # 保存提供给大模型的工具定义
        self.tools = []

        # 工具分发表
        # 根据模型返回的工具名称，找到对应的 Python 方法
        self.tool_dispatch = {}

        # 注册计算器工具
        self.register_tool(calculator_tool, self.show_calc)

        # 注册时间工具
        self.register_tool(time_tool, self.show_time)

        # 创建聊天记录管理器
        self.conversation_manager = ConversationManager(
            self.system_prompt
        )

        # 从 messages.json 加载历史聊天记录
        # 如果没有可用的记录，则由 ConversationManager 创建初始消息
        self.messages = self.conversation_manager.load_messages()

        # 初始化日志对象
        self.logger = setup_logger()

        # 记录程序初始化成功
        self.logger.info("ChatBot 初始化成功")

        print("ChatBot 创建成功！")

    # ==================== 4. 聊天主流程 ====================

    def chat(self):
        """
        负责一次完整的用户交互：

        获取输入 → 判断退出 → 处理命令
        → 保存用户消息 → 请求 AI
        → 保存 AI 回答 → 输出结果

        返回 True：继续下一轮聊天
        返回 False：退出聊天循环
        """

        # 获取用户输入
        user_input = input("\n你：")

        # 用户输入 exit，结束主循环
        if user_input == "exit":
            return False

        # 优先检查是不是 /help、/clear 等本地命令
        # 如果命令已处理，就不需要请求大模型
        if self.handle_command(user_input):
            return True

        # 将用户消息加入对话列表
        # role 用于区分消息是谁发送的
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )
        original_length = len(self.messages)
        # 调用大模型，获取回答
        answer = self.ask_ai()

        if answer is None:
            # 回滚本轮聊天新增的消息
            del self.messages[original_length:]

            print("AI 请求失败，请稍后重试。")
            return True

        # 请求成功，保存 AI 回答
        self.messages.append({
            "role": "assistant",
            "content": answer
        })

        self.conversation_manager.save_messages(self.messages)

        print(f"\nAI：{answer}")
        return True

        # 返回 True，让 while 循环继续
        return True

    # ==================== 5. 大模型请求与工具调用 ====================

    def ask_ai(self):
        """
        负责与大模型交互。

        当前支持两种情况：

        情况一：模型直接回答
            请求模型 → 返回回答

        情况二：模型需要调用工具
            请求模型 → 获取工具调用信息
            → 执行 Python 工具
            → 把工具结果交还给模型
            → 获取最终回答

        当前版本只处理模型返回的第一个工具调用。
        """
        original_length = len(self.messages)

        try:
            # 记录模型请求日志
            self.logger.info(
                "开始请求大模型，模型：%s",
                self.model
            )
            
            # 第一次请求大模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                # stream=True
            )

            # 获取模型返回的第一条消息
            message = response.choices[0].message

            # 如果模型没有请求调用工具
            # 说明这次可以直接返回文本回答
            if not message.tool_calls:
                return message.content

            # 如果模型请求了工具：
            # 先保存模型发出的工具调用消息
            #
            # model_dump() 将 SDK 消息对象转换为字典
            # 方便加入 self.messages
            self.messages.append(message.model_dump())

            # 获取第一个工具调用
            tool_call = message.tool_calls[0]

            # 获取工具名称，例如 calculator 或 time
            tool_name = tool_call.function.name

            # 记录工具调用日志
            self.logger.info(
                "模型请求调用工具：%s",
                tool_name
            )

            # 模型返回的 arguments 通常是 JSON 字符串
            # json.loads() 将 JSON 字符串转换为 Python 对象
            #
            # 例如：
            # '{"expression": "2+3"}'
            # 转换为：
            # {"expression": "2+3"}
            arguments = json.loads(
                tool_call.function.arguments
            )

            # 根据工具名称，从字典中找到对应的 Python 方法
            # get() 在找不到工具时返回 None
            tool = self.tool_dispatch.get(tool_name)

            if tool is None:
                raise ValueError(f"未知工具：{tool_name}")
            # 执行工具
            #
            # **arguments 表示字典解包
            # 例如：
            # {"expression": "2+3"}
            #
            # tool(**arguments)
            # 相当于：
            # tool(expression="2+3")
            result = tool(**arguments)

            # 将工具执行结果追加到消息列表
            #
            # tool_call_id 用于告诉模型：
            # 这条工具结果对应哪一次工具调用
            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            )

            # 第二次请求大模型
            # 这次把工具执行结果也发送给模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )

            # 获取模型结合工具结果生成的最终回答
            answer = response.choices[0].message.content

            return answer


        except Exception:

            # 删除本次 ask_ai() 新增的不完整消息
            del self.messages[original_length:]
            # 记录完整错误信息
            self.logger.exception("AI 请求或工具调用失败")
            # None 表示本次请求失败
            return None
    # ==================== 6. 聊天记录管理 ====================

    def clear_messages(self, argument=""):
        """
        清空聊天记录。

        ConversationManager 会重置记录，
        通常保留一条 system 消息。
        """

        self.messages = self.conversation_manager.clear_messages()

        print("聊天记录已清空！")

    def show_history(self, argument=""):
        """
        遍历消息列表，显示历史对话。
        """

        for message in self.messages:
            # 获取消息角色
            role = message["role"]

            # 获取消息内容
            # 工具调用消息的 content 可能为 None
            content = message.get("content")

            if role == "system":
                print("系统：", content)

            elif role == "user":
                print("你：", content)

            elif role == "assistant":
                print("AI：", content)

    # ==================== 7. 本地命令处理 ====================

    def handle_command(self, user_input):
        """
        判断用户输入是否为已注册的命令。

        例如：
        /calc 2+3

        拆分为：
        command = "/calc"
        argument = "2+3"
        """

        # maxsplit=1 表示最多分割一次
        parts = user_input.split(maxsplit=1)

        # 如果用户只输入空格，parts 会是空列表
        if not parts:
            return True

        # 第一部分是命令名称
        command = parts[0]

        # 如果存在第二部分，就作为命令参数
        if len(parts) > 1:
            argument = parts[1]
        else:
            argument = ""

        # 查找命令是否已注册
        if command in self.commands:
            # 取出对应的方法并执行
            self.commands[command](argument)
            return True

        # 不是已注册命令，交给聊天流程处理
        return False

    def show_help(self, argument=""):
        """显示帮助信息。"""
        print(help_text)

    def show_model(self, argument=""):
        """显示当前使用的模型。"""
        print(f"当前模型：{self.model}")

    def show_time(self, argument=""):
        """
        调用时间工具，返回当前时间。

        注意：这里只返回字符串。
        通过 /time 命令调用时，当前代码不会自动打印结果。
        """
        return self.time_tool.run()

    def show_calc(self, expression=""):
        """
        调用计算器工具。

        expression 是需要计算的数学表达式，
        例如 "2+3"。
        """
        try:
            result = self.calculator.run(expression)

            # 工具结果统一转换为字符串
            return str(result)

        except ValueError as e:
            # 当前实现将计算错误转换为字符串返回
            return str(e)

    # ==================== 8. 工具注册 ====================

    def register_tool(self, tool, func):
        """
        将一个工具注册到 ChatBot。

        tool：提供给大模型的工具说明字典
        func：真正负责执行工具的 Python 方法

        例如：
        register_tool(calculator_tool, self.show_calc)
        """

        # 把工具说明加入工具列表
        self.tools.append(tool)

        # 从工具说明中读取名称
        tool_name = tool["function"]["name"]

        # 建立“工具名称 → Python 方法”的映射
        self.tool_dispatch[tool_name] = func


# ==================== 9. 程序入口 ====================

# 创建 ChatBot 实例
# 会自动调用 ChatBot.__init__()
bot = ChatBot()

# 每次循环执行一轮聊天
# chat() 返回 False 时退出循环
while bot.chat():
    pass

print("程序结束")
