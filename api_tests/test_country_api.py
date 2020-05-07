from requests import get, post, put, delete

country_api_server = 'http://cloths-shop-prorotype.herokuapp.com/api/countries'
# # 'id', 'title' - возможные поля, используемые в бд
# """Для выполнения корректного запроса требуется заполнение всех полей модели !"""
# """Корректные"""
# """CountryListResource"""
# print(get(country_api_server).json())
# print(post(country_api_server, json={'id': 2, 'title': 'Италия'}).json())
# print(get(country_api_server).json())  # проверка добавления
# """CountryResource"""
# print(get(country_api_server).json())  # проверка исходных значений
# print(get(country_api_server + '/2').json())  # получение страны по id
# print(put(country_api_server + '/2', json={'id': 2, 'title': 'США'}).json())  # изменение по id
# print(get(country_api_server + '/2').json())  # подтверждение изменения
# print(delete(country_api_server + '/2').json())  # удаление по id
# print(delete(country_api_server + '/2').json())  # подтверждение удаления
# print(get(country_api_server).json())  # проверка результатов
# """Некорректные"""
"""CountryListResource"""
# лишний слэш (/) API считает за пустой аргумент id -> неверно
print(get('http://cloths-shop-prorotype.herokuapp.com/api/countries/').json())
print(post(country_api_server, json={'title': 'Италия'}).json())  # пропущено поле id
# id не может быть строкой - str. type(id) == int
print(post(country_api_server, json={'id': 'abc', 'title': 'Италия'}).json())
