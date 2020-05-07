from requests import get, post, put, delete

country_api_server = 'http://localhost:5000/api/countries'
# 'id', 'title' - возможные поля, используемые в бд
"""
Корректные
"""
"""CountryListResource"""
print(get(country_api_server).json())
print(post(country_api_server, json={'id': 25, 'title': 'Россия'}).json())
print(get(country_api_server).json())  # проверка добавления
"""CountryResource"""
print(get(country_api_server).json())  # проверка исходных значений
print(get(country_api_server + '/1').json())  # получение страны по id
print(put(country_api_server + '/1', json={'id': 1, 'title': 'США'}).json())  # изменение по id
print(get(country_api_server + '/1').json())  # подтверждение изменения
print(delete(country_api_server + '/1').json())  # удаление по id
print(delete(country_api_server + '/1').json())  # подтверждение удаления
print(get(country_api_server).json())  # проверка результатов
