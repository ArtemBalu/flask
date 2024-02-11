import requests
## Добавление нового пользователя
response = requests.post(
    'http://127.0.0.1:5000/user/',
    json={"name": "user_1", "password": "R#W@3rerete5$", "email": "Example@domen.com"},
)
print(response.status_code)
print(response.text)

## Получение заведомо существующего пользователя
response = requests.get(
    'http://127.0.0.1:5000/user/1/',
)
print(response.status_code)
print(response.text)

## Получение заведомо несуществующего пользователя
response = requests.get(
    'http://127.0.0.1:5000/user/600/',
)
print(response.status_code)
print(response.text)

## Изменение данных пользователя (некорректный пароль)
response = requests.patch(
    'http://127.0.0.1:5000/user/1/',
    json={"name": "new_user_2", "password": "R"}
)
print(response.status_code)
print(response.text)

## Изменение данных пользователя (корректный пароль)
response = requests.patch(
    'http://127.0.0.1:5000/user/1/',
    json={"name": "new_user_2", "password": "Rjhgfibue6yibwu3"}
)
print(response.status_code)
print(response.text)

## Проверка данных пользователя после изменения
response = requests.get(
    'http://127.0.0.1:5000/user/1/',
)
print(response.status_code)
print(response.text)

## Удаление пользователя
response = requests.delete(
    "http://127.0.0.1:5000/user/1/",
)
print(response.status_code)
print(response.text)

## Попытка получить удаленного пользователя
response = requests.get(
    "http://127.0.0.1:5000/user/1/",
)
print(response.status_code)
print(response.text)





## Добавление нового пользователя
response = requests.post(
    'http://127.0.0.1:5000/user/',
    json={"name": "user_1", "password": "R#W@3rerete5$", "email": "Example@domen.com"},
)
print(response.status_code)
print(response.text)

## Добавление нового объявления
response = requests.post(
    'http://127.0.0.1:5000/note/',
    json={"header": "Car", "description": "White, 4x4, 2021", "owner_id": 2},
)
print(response.status_code)
print(response.text)

## Получение заведомо существующего объявления
response = requests.get(
    'http://127.0.0.1:5000/note/1/',
)
print(response.status_code)
print(response.text)

## Получение заведомо несуществующего объявления
response = requests.get(
    'http://127.0.0.1:5000/note/600/',
)
print(response.status_code)
print(response.text)

## Изменение данных объявления
response = requests.patch(
    'http://127.0.0.1:5000/note/1/',
    json={"header": "Car SUV"}
)
print(response.status_code)
print(response.text)

## Проверка данных объявления после изменения
response = requests.get(
    'http://127.0.0.1:5000/note/1/',
)
print(response.status_code)
print(response.text)

## Удаление объявления
response = requests.delete(
    "http://127.0.0.1:5000/note/1/",
)
print(response.status_code)
print(response.text)

## Попытка получить удаленноe объявления
response = requests.get(
    "http://127.0.0.1:5000/note/1/",
)
print(response.status_code)
print(response.text)