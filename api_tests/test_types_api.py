from requests import get, post, put, delete

types_api_server = 'http://cloths-shop-project.herokuapp.com/api/types'
# 'id', 'title' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""TypesClothsListResource"""
print(get(types_api_server).json())
print(post(types_api_server, json={'title': 'Штапель_', 'api_key': 'r651I45H5P3Za45s'}).json())
print(get(types_api_server).json())  # проверка добавления
"""TypesClothsResource"""
print(get(types_api_server).json())  # проверка исходных значений
print(get(types_api_server + '/2').json())  # получение типа ткани по id
# изменение по id
print(put(types_api_server + '/2', json={'title': 'Штапель', 'api_key': 'r651I45H5P3Za45s'}).json())
print(get(types_api_server + '/2').json())  # подтверждение изменения
print(delete(types_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}).json())  # удаление по id
print(delete(types_api_server + '/2').json())  # подтверждение удаления
print(get(types_api_server).json())  # проверка результатов
"""Некорректные"""
"""TypesClothsListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/types/').json())
"""TypesClothsResource"""
print(get(types_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(types_api_server + "/787451188").json())
# то же, что и впредыдущем пункте
print(delete(types_api_server + "/787451188").json())
print(delete(types_api_server + "/7").json())  # нет api-ключа
# такого id нет
print(delete(types_api_server + "/abc", json={'api_key': 'r651I45H5P3Za45s'}).json())
print(put(types_api_server + '/2', json={}))  # пустой запрос
