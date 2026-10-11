# class Student:
#
#     def hello(self):
#         print(self)
#
# stu = Student()
#
# print(stu)
#
# stu.hello()
messages = [
    {"role": "system"},
    {"role": "user", "content": "你好"}
]

print(messages)

messages.pop()

print(messages)