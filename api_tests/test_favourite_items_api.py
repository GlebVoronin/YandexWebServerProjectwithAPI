from requests import get, post, put, delete

favourite_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/favourites'
# 'id', 'items_id' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""FavouriteItemsListResource"""
print(get(favourite_api_server).json())
print(post(favourite_api_server,
           json={'items_id': '', 'api_key': 'r651I45H5P3Za45s'}).json())
print(get(favourite_api_server).json())  # проверка добавления
"""FavouriteItemsResource"""
print(get(favourite_api_server).json())  # проверка исходных значений
print(get(favourite_api_server + '/2').json())  # получение избранного по id
# изменение по id
print(put(favourite_api_server + '/2',
          json={'items_id': '1;2', 'api_key': 'r651I45H5P3Za45s'}).json())
print(get(favourite_api_server + '/2').json())  # подтверждение изменения
print(delete(favourite_api_server + '/2',
             json={'api_key': 'r651I45H5P3Za45s'}).json())  # удаление по id
print(get(favourite_api_server + '/2').json())  # подтверждение удаления
print(get(favourite_api_server).json())  # проверка результатов
"""Некорректные"""
"""FavouriteItemsListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/favourites/').json())
# пустой запрос
print(post(favourite_api_server, json={'api_key': 'r651I45H5P3Za45s'}).json())
"""FavouriteItemsResource"""
print(get(favourite_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(favourite_api_server + "/787451188").json())
# то же, что и впредыдущем пункте
print(delete(favourite_api_server + "/787451188",
             json={'api_key': 'r651I45H5P3Za45s'}).json())
print(delete(favourite_api_server + "/7").json())  # нет API-ключа
print(delete(favourite_api_server + "/abc",
             json={'api_key': 'r651I45H5P3Za45s'}).json())  # такого id нет
print(put(favourite_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}))  # пустой запрос
# запрос без items_id, set - параметра напротив в api/favourites напротив нет
print(put(favourite_api_server + '/2', json={'set': ''}))  # пустой запрос
