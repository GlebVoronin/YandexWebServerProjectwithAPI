from flask import jsonify
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


class BaseResource(Resource):
    """
    Базовый класс ресурса для API, от которого наследуются классы для реальных моделей.
    Все методы универсальны для всех моделей, но могут быть переопределены при необходимости,
    так как используется наследование.
    Различаются последующие классы методом __init__, который у всех различен и, возможно,
    переопределёнными методами, если они будут необходимы.
    При большем числе моделей, возможно, будут нужны метаклассы.
    """

    def __init__(self, class_of_object, object_parser, list_of_args: tuple):
        self.class_of_object = class_of_object  # классы нужной модели
        self.parser = object_parser  # парсер для нужной модели
        self.list_of_arguments = list_of_args  # список полей в базе данных нужной модели

    def abort_if_object__not_found(self, object_id):
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
        self.abort_if_object__not_found(object_id)
        session = db_session.create_session()
        object_ = session.query(self.class_of_object).get(object_id)
        session.delete(object_)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, object_id):
        self.abort_if_object__not_found(object_id)
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

    def __init__(self, class_of_object, object_parser, list_of_args):
        self.class_of_object = class_of_object
        self.parser = object_parser
        self.list_of_arguments = list_of_args

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        object_ = self.class_of_object()  # создание объекта модели
        for arg_name in self.list_of_arguments:  # подстановка нужных полей и их значений
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


class MetaClass(type):
    def __new__(mcs, class_of_object, attrs, lst_class=False):
        name = class_of_object.__name__
        base = tuple(BaseListResource if lst_class else BaseResource)
        name += 'ListResource' if lst_class else 'Resource'
        dict_attrs = {'class_of_object': class_of_object, ''}
        return type.__new__(mcs, name, base, dict_attrs)


class UserResource(BaseResource):
    def __init__(self):
        super().__init__(User, user_parser, LIST_OF_ARGUMENTS_FOR_USER_RESOURCE)


class UserListResource(BaseListResource):
    def __init__(self):
        super().__init__(User, user_parser, LIST_OF_ARGUMENTS_FOR_USER_RESOURCE)


class ClothResource(BaseResource):
    def __init__(self):
        super().__init__(Cloth, cloth_parser, LIST_OF_ARGUMENTS_FOR_CLOTH_RESOURCE)


class ClothListResource(BaseListResource):
    def __init__(self):
        super().__init__(Cloth, cloth_parser, LIST_OF_ARGUMENTS_FOR_CLOTH_RESOURCE)


class OrderResource(BaseResource):
    def __init__(self):
        super().__init__(Order, order_parser, LIST_OF_ARGUMENTS_FOR_ORDER_RESOURCE)


class OrderListResource(BaseListResource):
    def __init__(self):
        super().__init__(Order, order_parser, LIST_OF_ARGUMENTS_FOR_ORDER_RESOURCE)


class FavouriteItemsResource(BaseResource):
    def __init__(self):
        super().__init__(FavouriteItems, favourite_parser, LIST_OF_ARGUMENTS_FOR_FAVOURITE_RESOURCE)


class FavouriteItemsListResource(BaseListResource):
    def __init__(self):
        super().__init__(FavouriteItems, favourite_parser, LIST_OF_ARGUMENTS_FOR_FAVOURITE_RESOURCE)


class CountryResource(BaseResource):
    def __init__(self):
        super().__init__(Country, country_parser, LIST_OF_ARGUMENTS_FOR_COUNTRY_RESOURCE)


class CountryListResource(BaseListResource):
    def __init__(self):
        super().__init__(Country, country_parser, LIST_OF_ARGUMENTS_FOR_COUNTRY_RESOURCE)
