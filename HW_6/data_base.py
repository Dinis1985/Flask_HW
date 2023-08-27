# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.

import databases
import sqlalchemy
from settings import settings

db = databases.Database(settings.DATABASE_URL)
meta_data = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         meta_data,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('name', sqlalchemy.String(32)),
                         sqlalchemy.Column('surname', sqlalchemy.String(32)),
                         sqlalchemy.Column('email', sqlalchemy.String(64)),
                         sqlalchemy.Column('password', sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table('products',
                            meta_data,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('title', sqlalchemy.String(32)),
                            sqlalchemy.Column('description', sqlalchemy.String(128)),
                            sqlalchemy.Column('price', sqlalchemy.Float),
                            )

orders = sqlalchemy.Table('orders',
                          meta_data,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                            nullable=False),
                          sqlalchemy.Column('product_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'),
                                            nullable=False),
                          sqlalchemy.Column('date', sqlalchemy.Date),
                          sqlalchemy.Column('status', sqlalchemy.String(32)),
                          )

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False})
meta_data.create_all(engine)