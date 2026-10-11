import json

# 保存
contacts = [
    {
        "name": "张三",
        "phone": "13800000001"
    },
    {
        "name": "李四",
        "phone": "13800000002"
    },
    {
        "name": "王五",
        "phone": "13800000003"
    }
]

with open("contacts.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(contacts, ensure_ascii=False))

# 读取
with open("contacts.json", "r", encoding="utf-8") as file:
    text = file.read()#字符串（String）

contacts = json.loads(text)#List

print(contacts)
print(type(contacts))