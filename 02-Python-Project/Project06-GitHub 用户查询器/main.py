import requests

def show_title():
    print("====== GitHub 用户查询器 ======")

show_title()

username = input("请输入 GitHub 用户名：")

url = f"https://api.github.com/users/{username}"

response = requests.get(url)

data = response.json()

print("\n====== 查询结果 ======")
print("用户名：", data["login"])
print("昵称：", data["name"])
print("粉丝数：", data["followers"])
print("公开仓库：", data["public_repos"])
print("主页：", data["html_url"])