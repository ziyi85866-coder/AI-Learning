# Function Calling 学习笔记（Agent 应用开发版）

> 目标：理解 Function Calling 是什么、为什么需要它、如何在项目中使用。

------------------------------------------------------------------------

# 1. Function Calling 是什么？

一句话：

> **让 LLM 决定什么时候调用你写的 Python 函数。**

没有 Function Calling：

``` text
用户：123*456 等于多少？
        │
        ▼
LLM 自己计算
        ▼
56088
```

有 Function Calling：

``` text
用户：123*456 等于多少？
        │
        ▼
LLM 判断：需要 Calculator
        │
        ▼
Python 执行 Calculator
        │
        ▼
56088
        │
        ▼
LLM 根据结果组织自然语言回答
```

**重点：LLM 不执行 Python，Python 也不会替代 LLM。**

------------------------------------------------------------------------

# 2. 为什么需要 Function Calling？

LLM 擅长：

-   对话
-   理解用户意图
-   组织自然语言

LLM 不擅长：

-   调数据库
-   查天气
-   调公司接口
-   操作文件
-   调用 Python 函数

因此需要 Function Calling，把 **LLM** 和 **Python** 连接起来。

------------------------------------------------------------------------

# 3. 一个 Tool 长什么样？

``` python
self.tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
```

## 字段说明

### type

固定写：

``` python
"type": "function"
```

表示这是一个函数工具。

### name

``` python
"calculator"
```

Tool 的唯一名称，LLM 根据它决定调用哪个 Tool。

### description

告诉 LLM：

> 什么时候应该调用这个 Tool。

### parameters

告诉 LLM：

> Tool 需要哪些参数。

------------------------------------------------------------------------

# 4. Function Calling 完整流程

``` text
① Python 发送 messages + tools
            │
            ▼
② LLM 判断是否需要 Tool
            │
            ▼
③ 返回 tool_calls
            │
            ▼
④ Python 解析 tool_calls
            │
            ▼
⑤ Python 执行 Tool
            │
            ▼
⑥ Tool 返回结果
            │
            ▼
⑦ Python 将 Tool Result 加入 messages
            │
            ▼
⑧ 第二次请求 LLM
            │
            ▼
⑨ LLM 生成最终回答
```

------------------------------------------------------------------------

# 5. 核心代码

## 第一次请求

``` python
response = client.chat.completions.create(
    model=self.model,
    messages=self.messages,
    tools=self.tools
)
```

------------------------------------------------------------------------

## 判断有没有 Tool

``` python
message = response.choices[0].message

if not message.tool_calls:
    return message.content
```

------------------------------------------------------------------------

## 获取 Tool

``` python
tool_call = message.tool_calls[0]
```

------------------------------------------------------------------------

## 获取 Tool 名称

``` python
tool_name = tool_call.function.name
```

例如：

``` text
calculator
```

------------------------------------------------------------------------

## 获取参数

``` python
arguments = json.loads(tool_call.function.arguments)
```

得到：

``` python
{
    "expression": "123*456"
}
```

------------------------------------------------------------------------

## 执行 Tool

``` python
expression = arguments["expression"]

result = self.show_calc(expression)
```

------------------------------------------------------------------------

## 保存 assistant(tool_call)

``` python
self.messages.append(message.model_dump())
```

注意：

不能：

``` python
self.messages.append(message)
```

因为：

`ChatCompletionMessage` 是 SDK 对象，不能直接 JSON 序列化。

------------------------------------------------------------------------

## 保存 Tool Result

``` python
self.messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result
})
```

------------------------------------------------------------------------

## 第二次请求

``` python
response = client.chat.completions.create(
    model=self.model,
    messages=self.messages
)
```

------------------------------------------------------------------------

## 返回最终回答

``` python
return response.choices[0].message.content
```

------------------------------------------------------------------------

# 6. 为什么要两次请求？

第一次：

LLM 决定调用哪个 Tool。

第二次：

LLM 根据 Tool 的结果组织最终回答。

Tool 负责 **数据**，LLM 负责 **语言**。

------------------------------------------------------------------------

# 7. 常见面试题

## Q1：Function Calling 是什么？

让 LLM
根据用户意图自动调用开发者提供的工具，并根据工具返回结果生成最终回答。

## Q2：为什么需要 tools？

告诉 LLM 当前有哪些工具可以使用，以及工具的作用和参数。

## Q3：为什么要 json.loads()？

因为 `function.arguments` 返回的是 JSON 字符串，需要转换成 Python 字典。

## Q4：为什么 show_calc() 要 return，而不是 print？

Tool 需要把结果返回给 Python，再由 Python 发给 LLM；print
只是输出到终端。

## Q5：为什么需要两次请求？

第一次获取 Tool Call，第二次根据 Tool Result 生成最终回复。

------------------------------------------------------------------------

# 8. 一定要记住的三句话

✅ Function Calling 不是 LLM 执行 Python，而是 **LLM 决定调用 Python**。

✅ Tool 负责计算和数据，LLM 负责自然语言回答。

✅ Agent 的核心流程：

``` text
LLM
  ↓
Tool Call
  ↓
Python Tool
  ↓
Tool Result
  ↓
LLM
```
