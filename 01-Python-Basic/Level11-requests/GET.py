# import requests
#
# response = requests.get("https://api.github.com")
#
# data = response.json()
#
# print("====== GitHub API ======")
#
# print(data["current_user_url"])
# print(data["repository_url"])
#
# print(data.keys())

import requests

response = requests.get("https://api.github.com/users/octocat")

data = response.json()

# print(data)
print(data["login"])
print(data["name"])
print(data["followers"])