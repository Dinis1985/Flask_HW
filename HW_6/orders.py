# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление

import users
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from models import *
from data_base import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# вывод заказов
@router.get('/orders/', response_model=list)
async def get_orders():
    query = sqlalchemy.select([orders, products, users]).where((
        users.c.id == orders.c.user_id) & (products.c.id == orders.c.product_id))
    rows = await db.fetch_all(query)
    return [
        Order(
            order=OrderIn(id=row[0], status=row[4], date=row[3], user_id=row[1], product_id=row[2]),
            user=User(id=row[9], name=row[10], surname=row[11], password=row[13], email=row[12], ),
            product=Product(id=row[5], title=row[6], description=row[7], price=row[8], ))
        for row in rows]


# размещение заказа
@router.post('/orders/', response_model=dict)
async def inp_orders(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        date=order.date,
        status=order.status)
    last_record_id = await db.execute(query)
    return {**order.dict(), "id": last_record_id}


# Просмотр одного заказа
@router.get("/order_id/{order_id}", response_model=OrderIn)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await db.fetch_one(query)


# Изменение информации о заказе
@router.put("/update_order/{order_id}", response_model=OrderIn)
async def update_order_information(order_id: int, update_order: OrderIn):
    query = orders.update() \
        .where(orders.c.id == order_id) \
        .values(**update_order.dict())
    await db.execute(query)
    return {**update_order.dict(), "id": order_id}


# Удаление заказа
@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {'message': 'Order deleted'}