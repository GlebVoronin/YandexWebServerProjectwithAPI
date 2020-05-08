from requests import get, post, put, delete

cloth_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/cloths'
# 'id', 'title', 'description', 'images_links', 'colors',
# 'length', 'price', 'date', 'country_id' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""ClothListResource"""
print(get(cloth_api_server).json())
images_links = '/static/img/cloth/image_23;/static/img/cloth/image_24;' \
               '/static/img/cloth/image_25;/static/img/cloth/image_26'
print(post(cloth_api_server, json={'title': 'Ткань_2', 'description': 'Описания\nнет',
                                   'images_links': images_links, 'colors': 'синий',
                                   'length': 120.0, 'price': 475,
                                   'date': 'None', 'country_id': 1,
                                   'api_key': 'r651I45H5P3Za45s'}).json())
print(get(cloth_api_server).json())  # проверка добавления
"""ClothResource"""
print(get(cloth_api_server).json())  # проверка исходных значений
print(get(cloth_api_server + '/2').json())  # получение избранного по id
# изменение по id
print(put(cloth_api_server + '/1', json={'title': 'Ткань_2', 'description': 'Описания\nнет',
                                         'images_links': images_links, 'colors': 'синий',
                                         'length': 247.0, 'price': 475,
                                         'date': 'None', 'country_id': 1,
                                         'api_key': 'r651I45H5P3Za45s'}).json())
print(get(cloth_api_server + '/2').json())  # подтверждение изменения
# удаление по id
print(delete(cloth_api_server + '/2', json={'api_key': 'r651I45H5P3Za45s'}).json())
print(get(cloth_api_server + '/2').json())  # подтверждение удаления
print(get(cloth_api_server).json())  # проверка результатов
"""Некорректные"""
"""ClothListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/cloths/').json())
print(post(cloth_api_server, json={}).json())  # пустой запрос
# country_id не заполнено
print(post(cloth_api_server, json={'title': 'Ткань_2', 'description': 'Описания\nнет',
                                   'images_links': images_links, 'colors': 'синий',
                                   'length': 120.0, 'price': 475,
                                   'date': 'None',
                                   'api_key': 'r651I45H5P3Za45s'}).json())
# Нет API-ключа
print(post(cloth_api_server, json={'title': 'Ткань_2', 'description': 'Описания\nнет',
                                   'images_links': images_links, 'colors': 'синий',
                                   'length': 120.0, 'price': 475,
                                   'date': 'None'}).json())
"""ClothResource"""
print(get(cloth_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(cloth_api_server + "/787451188").json())
print(delete(cloth_api_server + "/787451188").json())  # то же, что и впредыдущем пункте
# нет API-ключа
print(delete(cloth_api_server + "/7", json={'api_key': 'r651I45H5P3Za45s'}).json())
print(delete(cloth_api_server + "/abc").json())  # такого id нет
print(put(cloth_api_server + '/2', json={}))  # пустой запрос
# запрос без title и других параметров, set - параметра напротив в api/cloths
print(put(cloth_api_server + '/2', json={'set': ''}))
