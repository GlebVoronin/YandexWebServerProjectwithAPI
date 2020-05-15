from requests import get, post, put, delete

order_api_server = 'http://cloths-shop-project.herokuapp.com/api/orders'
# 'id', 'items_id', 'is_finished', 'status' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""OrderListResource"""
print(get(order_api_server).json())
print(post(order_api_server, json={'items_id': '', 'is_finished': False,
                                   'status': 'подготовка',
                                   'api_key': 'r651I45H5P3Za45s'}).json())
print(get(order_api_server).json())  # проверка добавления
"""OrderResource"""
print(get(order_api_server).json())  # проверка исходных значений
print(get(order_api_server + '/2').json())  # получение заказа по id
# изменение по id
print(put(order_api_server + '/2', json={'items_id': '', 'is_finished': False,
                                         'status': 'подготовка',
                                         'api_key': 'r651I45H5P3Za45s'}).json())
print(get(order_api_server + '/2').json())  # подтверждение изменения
# удаление по id
print(delete(order_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}).json())
print(get(order_api_server + '/2').json())  # подтверждение удаления
print(get(order_api_server).json())  # проверка результатов
"""Некорректные"""
"""OrderListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/orders/').json())
# is_finished - bool значение, не str
print(post(order_api_server, json={'items_id': '', 'is_finished': 'trr',
                                   'status': 'подготовка'}).json())
# пропущен параметр status
print(post(order_api_server, json={'items_id': '', 'is_finished': 'trr'}).json())
"""OrderResource"""
print(get(order_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(order_api_server + "/787451188").json())
print(delete(order_api_server + "/787451188",
             json={'api_key': 'r651I45H5P3Za45s'}).json())  # то же, что и впредыдущем пункте
print(delete(order_api_server + "/abc",
             json={'api_key': 'r651I45H5P3Za45s'}).json())  # такого id нет
print(put(order_api_server + '/2', json={}))  # пустой запрос
# is_finished пропущен
print(put(order_api_server + '/2', json={'items_id': '',
                                         'status': 'подготовка',
                                         'api_key': 'r651I45H5P3Za45s'}).json())
# is_finished str, а должен быть bool
print(put(order_api_server + '/2', json={'items_id': '', 'is_finished': 'a',
                                         'status': 'подготовка',
                                         'api_key': 'r651I45H5P3Za45s'}).json())
# пропущен API-ключ
print(put(order_api_server + '/2', json={'items_id': '', 'is_finished': True,
                                         'status': 'подготовка'}).json())
