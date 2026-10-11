import json

def show_title():
    print("====== 通讯录系统 ======")

def add_contact():
    name = input("请输入姓名:")
    phone = input("请输入电话:")
    # 简单查重
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
    save_contacts(contacts)
    print("添加成功！")

def update_contact():
    name = input("请输入要修改的姓名：")
    found = False
    for contact in contacts:
        if contact["name"] == name:
            phone = input("新的电话:")
            contact["phone"] = phone
            found = True
            save_contacts(contacts)
            print("修改成功！")
            break
    if not found:
        print("没有找到联系人！")

def delete_contact():
    name = input("请输入删除姓名：")
    found = False
    for contact in contacts:
        if contact["name"] == name:
            contacts.remove(contact)
            found = True
            save_contacts(contacts)
            print("删除成功！")
            break
    if not found:
        print("未找到联系人，删除失败！")

def load_contacts():
    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        # 文件不存在/损坏，返回默认三条数据
        return [
            {"name": "张三", "phone": "13800000001"},
            {"name": "李四", "phone": "13800000002"},
            {"name": "王五", "phone": "13800000003"}
        ]

def save_contacts(contacts_data):
    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(contacts_data, file, ensure_ascii=False, indent=2)

def show_contacts():
    if len(contacts) == 0:
        print("通讯录为空！")
        return
    for contact in contacts:
        print("姓名：", contact["name"])
        print("电话：", contact["phone"])
        print("-" * 20)

def main():
    global contacts
    # 程序启动加载json文件
    contacts = load_contacts()

    while True:
        show_title()
        print("1 查看联系人")
        print("2 添加联系人")
        print("3 修改联系人")
        print("4 删除联系人")
        print("5 退出")
        choice = input("请选择：")
        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("程序结束")
            break
        else:
            print("输入错误，请重新输入！")
    # 退出前保存一次
    save_contacts(contacts)

if __name__ == "__main__":
    main()
