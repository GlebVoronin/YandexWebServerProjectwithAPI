from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, IntegerField, FieldList,
                     BooleanField, MultipleFileField, FloatField, TextAreaField, SelectField,
                     SelectMultipleField)
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import DataRequired, Email
from data.validators import CheckStringFieldByDigit
from data.db_session import create_session, global_init
from data.models.cloth_groups_by_usage import TypesClothsByUsage
from data.models.cloth_groups_by_types import TypesCloths
from data.models.cloths import Cloth


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    email = EmailField('Электронная почта', validators=[DataRequired(), Email()])
    phone_number = StringField('Номер телефона')
    address = StringField('Адрес')
    postal_code = StringField('Почтовый индекс')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddClothForm(FlaskForm):
    DB_NAME = 'Main'
    global_init(f'db/{DB_NAME}.sqlite')
    session = create_session()
    types = [(str(type_.id), type_.title) for type_ in session.query(TypesCloths).all()]
    usages = [(str(usage.id), usage.title) for usage in session.query(TypesClothsByUsage).all()]
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    images = MultipleFileField('Фотографии')
    colors = StringField('Цвета', validators=[DataRequired()])
    length = FloatField('Доступная длина ткани (в метрах)', validators=[DataRequired()])
    price = IntegerField('Цена ткани (за 1 метр)', validators=[DataRequired()])
    country = StringField('Страна-производитель', validators=[DataRequired()])
    usage = SelectMultipleField(
        'Использование ткани', choices=usages, validators=[DataRequired()])
    type = SelectMultipleField(
        'Тип ткани', choices=types, validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class OrderForm(FlaskForm):
    count_list = FieldList(FloatField('Метров ткани (округление 0,1 метра)',
                                      validators=[DataRequired(), CheckStringFieldByDigit()]))
    submit = SubmitField('Перейте к оформлению заказа')


class OrderRegistrationForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired(), Email()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    postal_code = StringField('Почтовый индекс', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class SearchForm(FlaskForm):
    DB_NAME = 'Main'
    global_init(f'db/{DB_NAME}.sqlite')
    session = create_session()
    types = [(0, 'Все')]
    usages = [(0, 'Все')]
    types_length = session.query(TypesCloths).count()
    usages_length = session.query(TypesClothsByUsage).count()
    # подсчёт числа тканей по типам и использования тканей для отображения пользователю
    # используются словари для возможности удобного прохода по списку тканей 1 раз
    cloths_types = {str(key_id): 0 for key_id in range(1, types_length + 1)}
    cloths_usages = {str(key_id): 0 for key_id in range(1, usages_length + 1)}
    cloths = session.query(Cloth).all()
    # заполнение словарей данными о количестве типов и использований тканей
    for cloth in cloths:
        cloth_types = cloth.cloth_type_id.split(';')
        cloth_usages = cloth.cloth_type_by_usage_id.split(';')
        for _type in cloth_types:
            cloths_types[_type] += 1
        for _usage in cloth_usages:
            cloths_usages[_usage] += 1
    for type_ in session.query(TypesCloths).all():
        types.append((type_.id, type_.title + f': {cloths_types[str(type_.id)]}шт.'))
    for usage_ in session.query(TypesClothsByUsage).all():
        usages.append((usage_.id, usage_.title + f': {cloths_usages[str(usage_.id)]}шт.'))
    text = SearchField('Введите поисковый запрос')
    usage = SelectField('Использование ткани', choices=usages, coerce=int)
    type = SelectField('Тип ткани', choices=types, coerce=int)
    submit = SubmitField('Найти')
