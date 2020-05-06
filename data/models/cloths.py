import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Cloth(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cloths'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String(10000), nullable=False)
    """Ссылки на изображения на сервере, разделены ';'"""
    images_links = sqlalchemy.Column(sqlalchemy.String(1000), nullable=False)
    colors = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    length = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date)
    country_id = sqlalchemy.Column(sqlalchemy.ForeignKey('countries.id'))

    def get_images(self, all_images=False):
        if all_images:
            return self.images_links.split(';')
        else:
            return self.images_links.split(';')[0]

    def get_url(self):
        return f'/{self.id}'
