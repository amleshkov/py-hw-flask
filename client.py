import requests

url = "http://localhost:5000/ad/5"

# data = {
#      "title": "Test title",
#      "description": "Test description",
#      "user": 1,
#     }
response = requests.get(url)
print(response.status_code)
print(response.text)
