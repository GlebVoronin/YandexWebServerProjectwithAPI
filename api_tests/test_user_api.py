from requests import get, post, put, delete

user_api_server = 'http://cloths-shop-project.herokuapp.com/api/users'
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""UserListResource"""
print(get(user_api_server, json={'api_key': 'r651I45H5P3Za45s'}).json())
"""UserResource"""
# получение страны по id
print(get(user_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}).json())
"""Некорректные"""
"""UserListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/users/',
          json={'api_key': 'r651I45H5P3Za45s'}).json())
print(post(user_api_server, json={}).json())  # нельзя применять post к user_api
"""UserResource"""
print(get(user_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(user_api_server + "/787451188", json={'api_key': 'r651I45H5P3Za45s'}).json())
# нет API-ключа
print(get(user_api_server + "/7").json())
print(delete(user_api_server + "/7").json())  # нельзя применять delete к user_api
print(put(user_api_server + "/abc", json={}).json())  # нельзя применять put к user_api
