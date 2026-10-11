import requests

api_key = "你的API Key"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(
    "https://httpbin.org/headers",
    headers=headers
)

print(response.json())