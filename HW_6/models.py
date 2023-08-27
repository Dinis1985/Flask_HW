# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).

import datetime
from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str = Field(title='Name', min_length=3, max_length=32)
    surname: str = Field(title='Surname', min_length=3, max_length=32)
    email: str = Field(title='Email', min_length=9, max_length=64)
    password: str = Field(title='Password', min_length=3, max_length=32)


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    title: str = Field(title='Title', min_length=3, max_length=32)
    description: str = Field(title='Description', min_length=3, max_length=128)
    price: float


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    id: int
    user_id: int = Field(title='User Id')
    product_id: int = Field(title='Product Id')
    date: datetime.date = Field(title='Date')
    status: str = Field(title='Status', default='Placed')


class Order(BaseModel):
    order: OrderIn
    user: User
    product: Product