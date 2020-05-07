import datetime
from PIL import Image
import logging
import os
from requests import get, post, delete, put, patch
from flask import (Flask, request, abort, render_template, redirect, jsonify, make_response)
from data import db_session
from data.models.users import User
from data.models.cloths import Cloth
from data.models.countries import Country
from data.models.orders import Order
from data.models.favourites import FavouriteItems
from data.forms import RegisterForm, LoginForm, AddClothForm, OrderForm, OrderRegistrationForm
from flask_login import (login_user, logout_user, login_required, LoginManager, current_user)
from flask_restful import Api
from resources import all_resources

CONFIG_FILE = './config.txt'
DIVISOR = ';'
ADMINISTRATOR_PASSWORD = 'r651I45H5P3Za45s'
COUNT_OF_CLOTHS_BY_ONE_PAGE = 30
DB_NAME = 'Main'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init(f'db/{DB_NAME}.sqlite')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(all_resources.UserListResource, '/api/users')
api.add_resource(all_resources.UserResource, '/api/users/<int:object_id>')
api.add_resource(all_resources.FavouriteItemsListResource, '/api/favourites')
api.add_resource(all_resources.FavouriteItemsResource, '/api/favourites/<int:object_id>')
api.add_resource(all_resources.ClothListResource, '/api/cloths')
api.add_resource(all_resources.ClothResource, '/api/cloths/<int:object_id>')
api.add_resource(all_resources.CountryListResource, '/api/countries')
api.add_resource(all_resources.CountryResource, '/api/countries/<int:object_id>')
api.add_resource(all_resources.OrderListResource, '/api/orders')
api.add_resource(all_resources.OrderResource, '/api/orders/<int:object_id>')


def find_cloth_by_id(cloth_id):
    session = db_session.create_session()
    cloth = session.query(Cloth).filter(Cloth.id == cloth_id).first()
    return cloth


def find_cloths_by_id(cloths_id_str: list):
    """Возвращает список тканей(объектов) по списку их id"""
    session = db_session.create_session()
    cloths = []
    for index in cloths_id_str:
        cloth = session.query(Cloth).filter(Cloth.id == index).first()
        if cloth:
            cloths.append(cloth)
    return cloths


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def administrator_required(page_function):
    def wrapped(*args):
        if current_user.account_type != 'Администратор':
            return redirect('/')
        else:
            page_function(*args)

    return wrapped


def save_images(images: list):
    """Функция сохраняет изображения на сервере, возвращает имена файлов"""
    config_file = open(CONFIG_FILE, 'r', encoding='utf-8')
    """Индекс последнего изображения в config-файле"""
    index_data, other_data = list(), list()
    for line in config_file.readlines():
        if 'IMAGES_INDEX' in line:
            index_data.append(line)
        else:
            other_data.append(line)
    image_index = int(index_data[0].split('==')[1])
    config_file.close()
    for index, image in enumerate(images):
        file = open(f'./static/img/cloth/image_{image_index}.png', 'wb')
        file.write(image.stream.read())
        file.close()
        image = Image.open(f'./static/img/cloth/image_{image_index}.png')
        image = image.resize((1024, 1024), Image.LANCZOS)
        if index == 0:
            image.save(f'./static/img/cloth/image_{image_index + 1}.png')
            image = image.resize((256, 256), Image.LANCZOS)
            image.save(f'./static/img/cloth/image_{image_index}.png')
            image_index += 2
        else:
            image_index += 1
    config_file = open(CONFIG_FILE, 'w', encoding='utf-8')
    other_data.append(f'\nIMAGES_INDEX=={image_index}')  # обновление индекса последнего изображения
    config_file.writelines(other_data)
    config_file.close()
    file_names = [f'/static/img/cloth/image_{image_index - i - 1}.png' for i in range(len(images) + 1)]
    return list(reversed(file_names))


@app.route('/')
def main_page():
    session = db_session.create_session()
    cloths = list(session.query(Cloth).order_by(Cloth.date))
    """!!!Возможно требуется reversed(list)!!!///////////////////////////////////////////////////////"""
    if len(cloths) > COUNT_OF_CLOTHS_BY_ONE_PAGE:
        cloths = cloths[:COUNT_OF_CLOTHS_BY_ONE_PAGE]  # тканей не страницу
    countries_db = session.query(Country).all()
    countries = {}
    for country in countries_db:
        if country.id not in countries:
            countries[country.id] = country.title
    for cloth in cloths:
        cloth.country_id = countries.get(cloth.country_id, None)

    return render_template('main_page.html', cloths=cloths)


@app.route('/view/<int:cloth_id>')
def view_cloth(cloth_id):
    cloth = find_cloth_by_id(cloth_id)
    return render_template('view_cloth.html', cloth=cloth)


@app.route('/view/image/<link>')
def view_image(link):
    return render_template('view_image.html', link=link)


@login_required
@app.route('/favourites/<cloth_id>')
def add_cloth_to_favourites(cloth_id):
    session = db_session.create_session()
    cloth = find_cloth_by_id(cloth_id)
    if cloth:
        favourite_items = session.query(FavouriteItems).filter(
            FavouriteItems.id == current_user.favourite_id).first()
        current_user.favourite_id = favourite_items.id
        if favourite_items.items_id:
            items = favourite_items.items_id.split(DIVISOR)
            if cloth_id not in items:
                items.append(cloth_id)
                items = DIVISOR.join(items)
                favourite_items.items_id = items
                session.commit()
        else:
            favourite_items.items_id = cloth_id
            session.commit()
    return '<script>document.location.href = document.referrer</script>'


@login_required
@app.route('/favourites/delete/<cloth_id>')
def delete_cloth_from_favourites(cloth_id):
    session = db_session.create_session()
    favourite_items = session.query(FavouriteItems).filter(
        FavouriteItems.id == current_user.favourite_id).first()
    items = favourite_items.items_id.split(DIVISOR)
    new_items = []
    for item in items:
        if item != cloth_id:
            new_items.append(item)
    items = DIVISOR.join(new_items)
    favourite_items.items_id = items
    session.commit()
    return '<script>document.location.href = document.referrer</script>'


@login_required
@app.route('/order/delete/<cloth_id>')
def delete_cloth_from_order(cloth_id):
    session = db_session.create_session()
    order = session.query(Order).filter(
        Order.id == current_user.order_id).first()
    items = order.items_id.split(DIVISOR)
    new_items = []
    for item in items:
        if item != cloth_id:
            new_items.append(item)
    items = DIVISOR.join(new_items)
    order.items_id = items
    session.commit()
    return '<script>document.location.href = document.referrer</script>'


@login_required
@app.route('/order/<cloth_id>')
def add_cloth_to_order(cloth_id):
    session = db_session.create_session()
    cloth = find_cloth_by_id(cloth_id)
    if cloth:
        order = session.query(Order).filter(
            Order.id == current_user.order_id).first()
        if order.items_id:
            items = order.items_id.split(DIVISOR)
            if cloth_id not in items:
                items.append(cloth_id)
                items = DIVISOR.join(items)
                order.items_id = items
                session.commit()
        else:
            order.items_id = cloth_id
            session.commit()
    return '<script>document.location.href = document.referrer</script>'


@login_required
@app.route('/order', methods=['GET', 'POST'])
def view_order(form_data=[]):
    """
    form_data=[] для доступа к необходимым длинам ткани
    используется особенность питона с сохранением изменённых параметров по умолчанию
    """
    form = OrderForm()
    order_registration_form = OrderRegistrationForm()
    need_count = request.args.get('count', default=False, type=bool)
    confirm_order = request.args.get('confirm', default=False, type=bool)
    session = db_session.create_session()
    order = session.query(Order).filter(Order.id == current_user.order_id).first()
    items_id_in_order = order.items_id.split(';')
    cloths = []
    for index in items_id_in_order:
        cloth = session.query(Cloth).filter(Cloth.id == index).first()
        if cloth:
            cloths.append(cloth)
    length = list(range(len(cloths)))
    if not form.count_list:
        for i in length:
            form.count_list.append_entry()
    order_summ = 0
    if need_count:
        for index in range(len(cloths)):
            if form.count_list[index].data:
                order_summ += form.count_list[index].data * cloths[index].price
    if form.validate_on_submit() and confirm_order:
        form_data.append([entry.data for entry in form.count_list])
        user = session.query(User).filter(User.id == current_user.id).first()
        order_registration_form.surname.data = user.surname
        order_registration_form.name.data = user.name
        order_registration_form.middle_name.data = user.middle_name
        order_registration_form.email.data = user.email
        order_registration_form.phone_number.data = user.phone_number
        order_registration_form.address.data = user.address
        order_registration_form.postal_code.data = user.postal_code
        return render_template('order_registration.html', cloths=cloths, err=False,
                               length=length, form=order_registration_form)
    elif order_registration_form.is_submitted() and confirm_order:
        if order_registration_form.validate_on_submit():
            for index in range(len(cloths)):
                cloths[index].length -= form_data[0][index]
            order.status = f'ожидает отправки, id пользователя=={current_user.id}'
            user = session.query(User).filter(User.id == current_user.id).first()
            order = Order(items_id='', status='подготовка', is_finished=False)
            session.add(order)
            session.commit()
            user.order_id = order.id
            session.commit()
            return render_template('success_order_registration.html')
        else:
            user = session.query(User).filter(User.id == current_user.id).first()
            order_registration_form.surname.data = user.surname
            order_registration_form.name.data = user.name
            order_registration_form.middle_name.data = user.middle_name
            order_registration_form.email.data = user.email
            order_registration_form.phone_number.data = user.phone_number
            order_registration_form.address.data = user.address
            order_registration_form.postal_code.data = user.postal_code
            return render_template('order_registration.html', cloths=cloths, err=True,
                                   length=length, form=order_registration_form)
    return render_template('view_cloths_in_order.html', cloths=cloths, form=form,
                           length=length, count=need_count, summ=order_summ)


@login_required
@app.route('/favourites')
def view_favourites():
    session = db_session.create_session()
    favourites = session.query(FavouriteItems).filter(
        FavouriteItems.id == current_user.favourite_id).first()
    items_id_in_favourites = favourites.items_id.split(';')
    cloths = find_cloths_by_id(items_id_in_favourites)
    return render_template('view_cloths_in_favourites.html', cloths=cloths)


@login_required
@administrator_required
@app.route('/add_cloth', methods=['GET', 'POST'])
def add_cloth():
    form = AddClothForm()
    if form.errors:
        print(form.errors)
    if form.validate_on_submit():
        session = db_session.create_session()
        if (session.query(Cloth).filter(Cloth.title == form.title.data).first()
                and session.query(Cloth).filter(Cloth.length == form.length.data).first()):
            return render_template('add_cloth.html', title='Добавление ткани',
                                   form=form, message='Такая ткань уже есть')
        country = session.query(Country).filter(Country.title == form.country.data).first()
        if country is None:
            country = Country(title=form.country.data)
            session.add(country)
            session.commit()
            country = session.query(Country).filter(Country.title == form.country.data).first()
        country_id = country.id
        date = datetime.datetime.now()
        images = request.files.getlist('images')
        file_names = ';'.join(save_images(images))
        cloth = Cloth(
            title=form.title.data,
            description=form.description.data,
            images_links=file_names,
            colors=form.colors.data,
            length=form.length.data,
            price=form.price.data,
            date=date,
            country_id=country_id
        )
        session.add(cloth)
        session.commit()
        return redirect('/')
    return render_template('add_cloth.html', title='Добавление ткани', form=form)


@login_required
@administrator_required
@app.route('/<int:cloth_id>', methods=['GET', 'POST'])
def edit_cloth(cloth_id):
    form = AddClothForm()
    if request.method == "GET":
        session = db_session.create_session()
        cloth = session.query(Cloth).filter(Cloth.id == cloth_id).first()
        if cloth:
            form.title.data = cloth.title
            form.description.data = cloth.description
            form.colors.data = cloth.colors
            form.length.data = cloth.length
            form.price.data = cloth.price
            country = session.query(Country).filter(Country.title == cloth.country_id).first()
            form.country.data = country
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        cloth = session.query(Cloth).filter(Cloth.id == cloth_id).first()
        if cloth:
            country = session.query(Country).filter(Country.title == form.country.data).first()
            if country is None:
                country = Country(title=form.country.data)
                session.add(country)
                session.commit()
                country = session.query(Country).filter(Country.title == form.country.data).first()
            country_id = country.id
            date = datetime.datetime.now()
            images = request.files.getlist('images')
            file_names = ';'.join(save_images(images))
            cloth.title = form.title.data
            cloth.date = date
            cloth.images_links = file_names
            cloth.description = form.description.data
            cloth.images_links = file_names
            cloth.colors = form.colors.data
            cloth.length = form.length.data
            cloth.price = form.price.data
            cloth.country = country_id
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_cloth.html', title='Редактирование ткани', form=form)


@login_required
@administrator_required
@app.route('/delete/<int:cloth_id>', methods=['GET', 'POST'])
def delete_cloth(cloth_id):
    session = db_session.create_session()
    cloth = session.query(Cloth).filter(Cloth.id == cloth_id).first()
    if cloth:
        session.delete(cloth)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        order = Order(is_finished=False, status="подготовка", items_id='')
        favourite_items = FavouriteItems(items_id='')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            middle_name=form.middle_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            postal_code=form.postal_code.data,
            order=order,
            favourites=favourite_items)
        if form.password.data != form.password_repeat.data:
            if form.password_repeat.data != ADMINISTRATOR_PASSWORD:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            else:
                user.set_administrator()
        user.set_password(form.password.data)
        time = datetime.datetime.now()
        user.set_date_time(time)
        session.add(favourite_items)
        session.add(order)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 33507))
