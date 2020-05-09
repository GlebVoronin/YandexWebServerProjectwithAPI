from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, IntegerField, FieldList,
                     BooleanField, MultipleFileField, FloatField, TextAreaField, SelectField)
from wtforms.fields.html5 import EmailField, SearchField
from wtforms.validators import DataRequired, Email
from data.validators import CheckStringFieldByDigit
from data.db_session import create_session, global_init
from data.models.cloth_groups_by_usage import TypesClothsByUsage
from data.models.cloth_groups_by_types import TypesCloths


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
    types = [(type_.id, type_.title) for type_ in session.query(TypesCloths).all()]
    usages = [(usage.id, usage.title) for usage in session.query(TypesClothsByUsage).all()]
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    images = MultipleFileField('Фотографии')
    colors = StringField('Цвета', validators=[DataRequired()])
    length = FloatField('Доступная длина ткани (в метрах)', validators=[DataRequired()])
    price = IntegerField('Цена ткани (за 1 метр)', validators=[DataRequired()])
    country = StringField('Страна-производитель', validators=[DataRequired()])
    usage = SelectField('Использование ткани', choices=usages, coerce=int, validators=[DataRequired()])
    type = SelectField('Тип ткани', choices=types, coerce=int, validators=[DataRequired()])
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
    types.extend([(type_.id, type_.title) for type_ in session.query(TypesCloths).all()])
    usages.extend([(usage.id, usage.title) for usage in session.query(TypesClothsByUsage).all()])
    text = SearchField('Введите поисковый запрос')
    usage = SelectField('Использование ткани', choices=usages, coerce=int)
    type = SelectField('Тип ткани', choices=types, coerce=int)
    submit = SubmitField('Найти')
