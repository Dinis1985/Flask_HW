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

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Создание тестовых пользователей
@router.get("/add_test_users/{count}")
async def add_test_users(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(
            name=f'user_{i}',
            surname=f'smith_{i}',
            password=f'123{i}',
            email=f'user_{i}@mail.ru')
        await db.execute(query)
    return {'message': f'Added {count} test users'}


# Создание нового пользователя
@router.post("/add_user/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        password=user.password,
        email=user.email)
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}


# Вывести список пользователей
@router.get("/users/", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    return templates.TemplateResponse('user.html', {'request': request, 'users': await db.fetch_all(query)})


# Просмотр одного пользователя
@router.get("/user_id/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


# Изменение информации о пользователе
@router.put("/update_user/{user_id}", response_model=User)
async def update_user_information(user_id: int, update_user: UserIn):
    query = users.update() \
        .where(users.c.id == user_id) \
        .values(**update_user.dict())
    await db.execute(query)
    return {**update_user.dict(), "id": user_id}


# Удаление пользователя
@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}