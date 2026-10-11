import json

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
# file = open("contacts.json", "r", encoding="utf-8")
# file.read(json.loads(contacts, ensure_ascii=False))



#import json
# text = '{"name":"王五","score":98}'
#
# student = json.loads(text)
#
# print(student)
# print(type(student))