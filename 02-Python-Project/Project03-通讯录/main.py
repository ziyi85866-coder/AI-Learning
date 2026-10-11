def show_title():
     print("====== 通讯录系统 ======")
def add_contact():
    name = input("请输入姓名:")
    phone = input("请输入电话:")
    contacts.append(
        {
            "name": name,
            "phone": phone
        }
    )
def update_contact():
    name = input()
    found = False
    for contact in contacts:
        if contact["name"] == name:
            phone = input("新的电话:")
            contact["phone"] = phone
            found = True
            break
    else:
        print("没有找到联系人！")
def delete_contact():
    name = input("请输入删除姓名：")
    found = False
    for contact in contacts:
        if contact["name"] == name:
            contacts.remove(contact)
            found = True
            break
    print("删除成功！")
def load_contacts():
    try:
        with open("contacts.json", "r", encoding="utf-8") as file:
            return json.loads(file.read())

    except:
        return []


def save_contacts(contacts):
    with open("contacts.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(contacts, ensure_ascii=False))

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
        print("1 查看联系人")
        print("2 添加联系人")
        print("3 修改联系人")
        print("4 删除联系人")
        print("5 退出")
        print("请选择：")
        choice = input()
        if choice == "1":
            for contact in contacts:
                print(contact["name"])
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
main()
