import uvicorn
from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class InputUser(BaseModel):
    login: str
    password: str
    email: str
    description: Optional[str] = None


class User(InputUser):
    id: int


users = [
    User(id=1,
         login='Mop',
         password='12345',
         email='mop@mail.ru'
         )
]


@app.get("/", response_model=list[User])
async def users_list():
    return users


@app.post("/input_user/", response_model=User)
async def create_task(data: InputUser):
    id_u = len(users) + 1
    user = User(
        id=id_u,
        login=data.login,
        password=data.password,
        email=data.email,
        description=data.description
    )
    users.append(user)
    return user


@app.get("/user/{id}", response_model=User)
async def get_task_by_id_root(id_u: int):
    for user in users:
        if user.id == id_u:
            return user


@app.put("/rep_us/{id}", response_model=User)
async def replace_user(id_u: int, new_data: InputUser):
    for user in users:
        if user.id == id_u:
            user.login = new_data.login
            user.password = new_data.password
            user.email = new_data.email
            user.description = new_data.description
            return user
    raise HTTPException(status_code=404, detail="User not found!")


@app.delete("/del_user/{id}")
async def delete_user(id_u: int):
    for user in users:
        if user.id == id_u:
            users.remove(user)
            return users
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/list_users/", response_class=HTMLResponse)
async def list_users(request: Request):
    return templates.TemplateResponse("db.html", {"request": request, 'users': users})


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        # host="127.0.0.1",
        # port=8000,
        reload=True
    )