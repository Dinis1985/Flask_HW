# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление

from fastapi import APIRouter
from models import *
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from data_base import *
from random import randint

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Создание тестовых продуктов
@router.get("/add_test_products/{count}")
async def add_test_products(count: int):
    for i in range(1, count + 1):
        query = products.insert().values(
            title=f'product_{i}',
            description=f'description_{i}',
            price=randint(1, 100000))
        await db.execute(query)
    return {'message': f'Added {count} test products'}


# Создание нового продукта
@router.post("/add_product/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(
        title=product.title,
        description=product.description,
        price=product.price)
    last_record_id = await db.execute(query)
    return {**product.dict(), "id": last_record_id}


# Вывести список продуктов
@router.get("/products/", response_class=HTMLResponse)
async def read_products(request: Request):
    query = products.select()
    return templates.TemplateResponse('products.html', {'request': request, 'products': await db.fetch_all(query)})


# Просмотр одного продукта
@router.get("/product_id/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await db.fetch_one(query)


# Изменение информации о продукте
@router.put("/update_product/{product_id}", response_model=Product)
async def update_user_information(product_id: int, update_product: ProductIn):
    query = products.update() \
        .where(products.c.id == product_id) \
        .values(**update_product.dict())
    await db.execute(query)
    return {**update_product.dict(), "id": product_id}


# Удаление продукта
@router.delete("/delete_product/{product_id}")
async def delete_user(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {'message': 'Product deleted'}