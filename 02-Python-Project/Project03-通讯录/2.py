# 打印标题
def show_title():
    print("====== 通讯录系统 ======")

# 查看全部联系人
def show_contacts():
    if len(contacts) == 0:
        print("通讯录为空！")
        return
    for contact in contacts:
        print("姓名:", contact["name"])
        print("电话:", contact["phone"])
        print("-" * 20)

# 添加联系人
def add_contact():
    name = input("请输入姓名:")
    phone = input("请输入电话:")
    # 简单判断：同名提示
    for c in contacts:
        if c["name"] == name:
            print("该联系人已存在！")
            return
    contacts.append(
        {
            "name": name,
            "phone": phone
        }
    )
    print("添加成功！")

# 修改联系人
def update_contact():
    name = input("请输入要修改的姓名:")
    found = False
    for contact in contacts:
        if contact["name"] == name:
            phone = input("请输入新的电话:")
            contact["phone"] = phone
            found = True
            print("修改成功！")
            break
    if not found:
        print("没有找到联系人！")

# 删除联系人
def delete_contact():
    name = input("请输入要删除的姓名：")
    found = False
    for contact in contacts:
        if contact["name"] == name:
            contacts.remove(contact)
            found = True
            print("删除成功！")
            break
    if not found:
        print("未找到该联系人，删除失败！")


# 初始化通讯录数据
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

# 主菜单循环
while True:
    show_title()
    print("1 查看联系人")
    print("2 添加联系人")
    print("3 修改联系人")
    print("4 删除联系人")
    print("5 退出")
    choice = input("请选择功能（输入数字）：")

    if choice == "1":
        show_contacts()
    elif choice == "2":
        add_contact()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        print("程序结束，再见！")
        break
    else:
        print("输入错误，请输入1~5之间的数字！")

    # 增加暂停，方便看结果，按回车继续菜单
    input("\n按回车键返回菜单...")
