"""Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
○ Имя пользователя (обязательное поле)
○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке."""

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from tasks.models import db, User
from tasks.forms import RegisterForm
from werkzeug.security import generate_password_hash
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

app.config['SECRET_KEY'] = b'bf64099707255eab2668980ffd15813b536725ba62fe6f52904a13d32463395f'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Hi!'


@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        birthdate = form.birthdate.data
        email = form.email.data
        password = form.password.data
        if not re.search('/d', password) and not re.search('[a-zA-Z]', password):
            error_msg = 'The password must contain at least one letter and at least one digit.'
            form.password.errors.append(error_msg)
            return render_template('register.html', form=form)
        existing_user = User.query.filter(
            (User.surname == surname) & (User.name == name) | (User.email == email)).first()
        if existing_user:
            error_msg = 'Username or email already exists.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)
        user = User(name=name, surname=surname, birthdate=birthdate, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return 'Registered success!'
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)