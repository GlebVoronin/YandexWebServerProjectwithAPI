from flask import jsonify
from flask.views import MethodViewType
from data import db_session
from flask_restful import abort, Resource
from data.models.users import User
from data.models.cloths import Cloth
from data.models.countries import Country
from data.models.orders import Order
from data.models.favourites import FavouriteItems
from parsers.user_parser import parser as user_parser
from parsers.cloth_parser import parser as cloth_parser
from parsers.order_parser import parser as order_parser
from parsers.favourite_parser import parser as favourite_parser
from parsers.country_parser import parser as country_parser

DICT_OF_ARGUMENTS_FOR_MODELS = {'User': ('id', 'surname', 'name', 'middle_name',
                                         'email', 'phone_number', 'address', 'postal_code',
                                         'hashed_password', 'register_date', 'order_id', 'favourite_id',
                                         'account_type'),
                                'Cloth': ('id', 'title', 'description', 'images_links', 'colors',
                                          'length', 'price', 'date', 'country_id'),
                                'Order': ('id', 'items_id', 'is_finished', 'status'),
                                'FavouriteItems': ('id', 'items_id'),
                                'Country': ('id', 'title')}
DICT_OF_PARSERS = {'User': user_parser,
                   'Cloth': cloth_parser,
                   'Order': order_parser,
                   'FavouriteItems': favourite_parser,
                   'Country': country_parser}

"""Классы должны быть созданы с помощью метакласса.
Создание объектов базовых классов не предусмотрено,
но от них могут наследоваться другие классы.
В данном случае должен быть объявлен метод __init__,
устанавливающий атрибуты class_of_object, parser, list_of_arguments
class_of_object - класс модели, для которой создается ресурс API
parser - парсер аргументов для json
list_of_arguments - список/кортеж, содержащий названия полей класса модели для базы данных 
"""


class BaseResource(Resource):
    """
    Базовый класс ресурса для API, от которого наследуются классы для реальных моделей.
    Все методы универсальны для всех моделей, но могут быть переопределены при необходимости,
    так как используется наследование.
    """

    def abort_if_object_not_found(self, object_id):
        """Проверка на наличие объекта с нужным id в базе данных"""
        session = db_session.create_session()
        object_ = session.query(self.class_of_object).get(object_id)  # объект нужной модели
        if not object_:
            # сообщение вида: Cloth 785 not found
            abort(404, message=f"{self.class_of_object.__name__} {object_id} not found")

    def get(self, object_id):
        self.abort_if_object_not_found(object_id)
        session = db_session.create_session()
        object_ = session.query(self.class_of_object).filter(self.class_of_object.id == object_id).first()
        return jsonify(
            {
                f'{self.class_of_object.__name__}':  # пример: {'Cloth': {id: 78, ...}}
                    object_.to_dict(only=self.list_of_arguments)
            }
        )

    def delete(self, object_id):
        self.abort_if_object_not_found(object_id)
        session = db_session.create_session()
        object_ = session.query(self.class_of_object).get(object_id)
        session.delete(object_)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, object_id):
        self.abort_if_object_not_found(object_id)
        session = db_session.create_session()
        object_ = session.query(self.class_of_object).filter(self.class_of_object.id == object_id).first()
        args = self.parser.parse_args()
        """установка значений аргументов для объекта модели self.class_of_object (эксперимент с setattr)"""
        for arg_name in self.list_of_arguments:
            setattr(object_, arg_name, args[arg_name])
        session.commit()
        return jsonify({'success': 'OK'})


class BaseListResource(Resource):
    """Класс, подобный предыдущему, для списка объектов моделей"""

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        object_ = self.class_of_object()  # создание объекта модели
        # подстановка нужных полей и их значений. [1:] т.к. первый аргумент - id
        # не требуется указывать
        for arg_name in self.list_of_arguments[1:]:
            setattr(object_, arg_name, args[arg_name])  # после создания объекта
        session.add(object_)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        objects = session.query(self.class_of_object).all()
        return jsonify(
            {  # пример: Cloths: [0: {id: 78, ...}, 1: {id: 79}...]
                f'{self.class_of_object.__name__}s':
                    [item.to_dict(only=self.list_of_arguments)
                     for item in objects]
            }
        )


class MetaClass(MethodViewType):
    """
    Метакласс. Создаёт классы API по нужной модели на основе базовых
    см. BaseResource, BaseListResource
    """

    def __init__(cls, cls_obj, lst=False):
        """
        Переопределение метода __init__ класса MethodViewType
        Это нужно только ради отсутствия конфликта метаклассов, так как
        MethodViewType - метакласс
        """
        pass

    def __new__(mcs, class_of_object, lst_class=False):
        name = class_of_object.__name__
        base = BaseListResource if lst_class else BaseResource
        # Аргументы при инициализации базового класса
        # Зависят от нужной модели (класса) - class_of_object
        # вместо подстановки в __init__ они добавляются при создании
        dict_attrs = {'class_of_object': class_of_object,
                      'parser': DICT_OF_PARSERS[name],
                      'list_of_arguments': DICT_OF_ARGUMENTS_FOR_MODELS[name]}
        name += 'ListResource' if lst_class else 'Resource'  # имя будущего класса
        return type.__new__(mcs, name, (base,), dict_attrs)  # возвращает class-объект


UserResource = MetaClass(User)
UserListResource = MetaClass(User, True)
ClothResource = MetaClass(Cloth)
ClothListResource = MetaClass(Cloth, True)
OrderResource = MetaClass(Order)
OrderListResource = MetaClass(Order, True)
FavouriteItemsResource = MetaClass(FavouriteItems)
FavouriteItemsListResource = MetaClass(FavouriteItems, True)
CountryResource = MetaClass(Country)
CountryListResource = MetaClass(Country, True)
