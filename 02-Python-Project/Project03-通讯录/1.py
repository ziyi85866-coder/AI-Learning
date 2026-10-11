def show_title():
    print("\n====== 通讯录系统 ======")


def show_contacts():
    if len(contacts) == 0:
        print("通讯录为空！")
        return

    for contact in contacts:
        print("姓名：", contact["name"])
        print("电话：", contact["phone"])
        print()


def add_contact():
    name = input("请输入姓名：")
    phone = input("请输入电话：")

    contacts.append({
        "name": name,
        "phone": phone
    })

    print("添加成功！")


def search_contact():
    name = input("请输入要查询的姓名：")

    found = False

    for contact in contacts:
        if contact["name"] == name:
            print("找到联系人！")
            print("姓名：", contact["name"])
            print("电话：", contact["phone"])
            found = True
            break

    if not found:
        print("没有找到联系人！")


def update_contact():
    name = input("请输入要修改的姓名：")

    found = False

    for contact in contacts:
        if contact["name"] == name:
            phone = input("请输入新的电话：")
            contact["phone"] = phone
            found = True
            print("修改成功！")
            break

    if not found:
        print("没有找到联系人！")


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
        print("没有找到联系人！")


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


def main():
    while True:
        show_title()

        print("1. 查看联系人")
        print("2. 添加联系人")
        print("3. 查询联系人")
        print("4. 修改联系人")
        print("5. 删除联系人")
        print("6. 退出")

        choice = input("请选择：")

        if choice == "1":
            show_contacts()

        elif choice == "2":
            add_contact()

        elif choice == "3":
            search_contact()

        elif choice == "4":
            update_contact()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            print("程序结束，再见！")
            break

        else:
            print("输入错误，请重新输入！")


main()