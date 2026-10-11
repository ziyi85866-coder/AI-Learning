file = open("test.txt", "w", encoding="utf-8")
file.write("你好！\n")
file.write("我是张子怡！\n")
file.write("今天开始学习Python文件！")
# with open("test.txt", "w", encoding="utf-8") as file:
#     file.write("你好")
file.close()
file = open("test.txt", "r", encoding="utf-8")
print(file.read())