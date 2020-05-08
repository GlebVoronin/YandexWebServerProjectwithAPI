from requests import get, post, put, delete

country_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/usage'
# 'id', 'title' - возможные поля, используемые в бд
"""Для выполнения корректного запроса требуется заполнение всех полей модели кроме id!"""
"""Корректные"""
"""CountryListResource"""
print(get(country_api_server).json())
print(post(country_api_server, json={'title': 'Италия'}).json())
print(get(country_api_server).json())  # проверка добавления
"""CountryResource"""
print(get(country_api_server).json())  # проверка исходных значений
print(get(country_api_server + '/2').json())  # получение страны по id
print(put(country_api_server + '/2', json={'title': 'США'}).json())  # изменение по id
print(get(country_api_server + '/2').json())  # подтверждение изменения
print(delete(country_api_server + '/2').json())  # удаление по id
print(delete(country_api_server + '/2').json())  # подтверждение удаления
print(get(country_api_server).json())  # проверка результатов
"""Некорректные"""
"""CountryListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/countries/').json())
"""CountryResource"""
print(get(country_api_server + "/abc").json())  # неверный id т.к. не int
# предположительно некорректный запрос. Вероятнее всего, такого id нет
print(get(country_api_server + "/787451188").json())
print(delete(country_api_server + "/787451188").json())  # то же, что и впредыдущем пункте
print(delete(country_api_server + "/abc").json())  # такого id нет
print(put(country_api_server + '/2', json={}))  # пустой запрос
