import requests

url = "https://httpbin.org/headers"

headers = {
    "User-Agent": "Python-Learning"
}

response = requests.get(url, headers=headers)

data = response.json()

print(data["headers"]["User-Agent"])