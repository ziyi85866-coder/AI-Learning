import requests

url = "https://httpbin.org/post"

data = {
    "name": "张子怡",
    "age": 23
}

response = requests.post(url, json=data)

print(response.status_code)

result = response.json()

# print(result)
# print(result["json"])
print(result["json"]["name"])
print(result["json"]["age"])