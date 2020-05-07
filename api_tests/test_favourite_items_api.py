from requests import get, post, put, delete

favourite_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/favourites'
# 'id', 'items_id' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""FavouriteItemsListResource"""
print(get(favourite_api_server).json())
print(post(favourite_api_server, json={'items_id': ''}).json())
print(get(favourite_api_server).json())  # проверка добавления
"""FavouriteItemsResource"""
print(get(favourite_api_server).json())  # проверка исходных значений
print(get(favourite_api_server + '/2').json())  # получение избранного по id
print(put(favourite_api_server + '/2', json={'items_id': '1;2'}).json())  # изменение по id
print(get(favourite_api_server + '/2').json())  # подтверждение изменения
print(delete(favourite_api_server + '/2').json())  # удаление по id
print(delete(favourite_api_server + '/2').json())  # подтверждение удаления
print(get(favourite_api_server).json())  # проверка результатов
"""Некорректные"""
"""FavouriteItemsListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/favourites/').json())
print(post(favourite_api_server, json={}).json())  # пустой запрос
"""FavouriteItemsResource"""
print(get(favourite_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(favourite_api_server + "/787451188").json())
print(delete(favourite_api_server + "/787451188").json())  # то же, что и впредыдущем пункте
print(delete(favourite_api_server + "/abc").json())  # такого id нет
print(put(favourite_api_server + '/2', json={}))  # пустой запрос
