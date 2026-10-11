第一章 ChatBot 项目
V1 ChatBot 基础版
学到的知识
- class
- init
- self
- 成员变量
- 成员方法
- 对象创建
项目实现
实现了：
class ChatBot:


封装了：
- client
- model
- messages
统一管理 ChatBot 状态。
面试指数
⭐⭐⭐⭐⭐
项目指数
⭐⭐⭐⭐⭐
Agent 指数
⭐⭐⭐⭐⭐
面试题
Q：什么是 self？
回答：
self 表示当前对象本身，用于访问对象中的成员变量和成员方法。
例如：
self.modelself.messages


Q：为什么使用 class？
回答：
因为 ChatBot 包含大量共享状态（client、messages、commands 等），使用类可以统一管理对象生命周期，提高代码可维护性。
简历亮点
基于 Python 面向对象思想设计 ChatBot，实现状态统一管理。

第二章 Chat 历史记录
学到的知识
- json
- json.loads()
- json.dumps()
- with open()
- UTF-8
项目实现
实现：
messages.json

自动保存聊天记录。
程序重新启动：
继续聊天。
面试指数
⭐⭐⭐⭐⭐
项目指数
⭐⭐⭐⭐⭐
Agent 指数
⭐⭐⭐⭐
面试题
Q：为什么不用 txt？
回答：
JSON 能保存列表和字典，方便恢复完整聊天上下文。
简历亮点
实现多轮上下文持久化，支持历史聊天恢复。

第三章 Stream 流式输出
学到的知识
stream=True


项目实现
实现：
AI 一个字一个字输出。

面试指数
⭐⭐⭐
项目指数
⭐⭐⭐⭐
Agent 指数
⭐⭐⭐⭐⭐
面试题
Q：为什么使用 Stream？
回答：
提升用户体验，降低等待时间。
简历亮点
基于 OpenAI SDK 实现流式响应。

第四章 Command Table
学到的知识
- 函数对象
- Command Table
- split(maxsplit=1)
项目实现
实现：
self.commands = {    "/help": self.show_help,    "/history": self.show_history,    "/time": self.show_time,}


替代大量：
if...elif...


面试指数
⭐⭐⭐⭐⭐
项目指数
⭐⭐⭐⭐⭐
Agent 指数
⭐⭐⭐⭐⭐
面试题
Q：为什么不用很多 if？
回答：
使用 Command Table 能够降低耦合，提高扩展性。
新增命令：
无需修改原有代码。
符合开闭原则。
Q：为什么 commands 放 init？
回答：
commands 属于整个 ChatBot 生命周期共享的数据，只需要初始化一次。
Q：为什么保存的是
self.show_help


不是：
self.show_help()


回答：
因为保存的是函数对象。
真正调用时：
self.commands[command]()


简历亮点
设计 Command Table，实现命令动态分发，提高系统扩展性。

第五章 Command Parsing
学到的知识
split(maxsplit=1)


项目实现
实现：
/help

↓

command

argument

支持：
/calc 1+2

命令与参数分离。
面试指数
⭐⭐
项目指数
⭐⭐⭐⭐⭐
Agent 指数
⭐⭐⭐⭐⭐
面试题
Q：为什么使用 split(maxsplit=1)？
回答：
保证参数中即使包含空格，也不会继续拆分。
简历亮点
实现命令解析模块（Command Parsing），支持命令与参数分离。

当前项目版本
V1 ChatBot                 ✅

V2 History                 ✅

V3 Stream                  ✅

V4 Command Table           ✅

V5 Command Parsing         ✅

V5.1 Calculator            🚧

V6 Tool Manager            ⏳

V7 Function Calling        ⏳

V8 MCP                     ⏳

V9 Agent                   ⏳

当前能力树
Python
├── class              ✅
├── self               ✅
├── __init__           ✅
├── 函数对象            ✅
├── JSON               ✅
├── 文件读写            ✅
├── split              ✅
├── eval               🚧
├── try...except       ⏳
└── 装饰器              ⏳

Agent
├── ChatBot            ✅
├── Stream             ✅
├── Tool               🚧
├── Tool Manager       ⏳
├── Function Calling   ⏳
├── MCP                ⏳
├── RAG                ⏳
└── Workflow           ⏳