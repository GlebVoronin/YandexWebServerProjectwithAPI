from requests import get, post, put, delete

usage_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/usage'
# 'id', 'title' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""TypesClothsByUsageListResource"""
print(get(usage_api_server).json())
print(post(usage_api_server, json={'title': 'Для брюк', 'api_key': 'r651I45H5P3Za45s'}).json())
print(get(usage_api_server).json())  # проверка добавления
"""TypesClothsByUsageResource"""
print(get(usage_api_server).json())  # проверка исходных значений
print(get(usage_api_server + '/2').json())  # получение использования ткани по id
# изменение по id
print(put(usage_api_server + '/2', json={'title': 'Для брюк',
                                         'api_key': 'r651I45H5P3Za45s'}).json())
print(get(usage_api_server + '/2').json())  # подтверждение изменения
# удаление по id
print(delete(usage_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}).json())
print(get(usage_api_server + '/2').json())  # подтверждение удаления
print(get(usage_api_server).json())  # проверка результатов
"""Некорректные"""
"""TypesClothsByUsageListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/usage/').json())
"""TypesClothsByUsageResource"""
print(get(usage_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(usage_api_server + "/787451188").json())
# то же, что и впредыдущем пункте
print(delete(usage_api_server + "/787451188").json())
print(delete(usage_api_server + "/7").json())  # нет api-ключа
# такого id нет
print(delete(usage_api_server + "/abc", json={'api_key': 'r651I45H5P3Za45s'}).json())
print(put(usage_api_server + '/2', json={}))  # пустой запрос
