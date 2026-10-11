def test():
    text = input("请输入：")

    if text == "exit":
        return False

    print("你输入的是：", text)

    return True


while test():
    pass

print("程序结束")