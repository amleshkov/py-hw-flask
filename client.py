import requests

BASE_URL = "http://localhost:5000"

# Регистрация нового пользователя

# data = {
#     "login": "admin",
#     "email": "admin@null.nl",
#     "password": "super_secret_password",
# }
# response = requests.post(f"{BASE_URL}/signup", json=data)
# public_id = response.json().get("data").get("public_id")
# print(response.status_code)
# print(response.json())
# print(public_id)

# Логин и получение JWT

data = {
    "email": "admin@null.nl",
    "password": "super_secret_password",
}
response = requests.post(f"{BASE_URL}/login", json=data)
print(response.status_code)
print(response.json())
cookies = response.cookies
print(cookies)

# Создаем объявление с кукой

data = {
    "title": "test",
    "description": "test with cookie",
}

response = requests.post(f"{BASE_URL}/ad", json=data, cookies=cookies)
print(response.status_code)
print(response.json())

# Изменяем свое объявление
data = {
    "title": "new test",
    "description": "changed",
}
response = requests.put(f"{BASE_URL}/ad/1", json=data, cookies=cookies)
print(response.status_code)
print(response.json())

# Удаляем свое объявление

response = requests.delete(f"{BASE_URL}/ad/1", cookies=cookies)
print(response.status_code)
print(response.json())
