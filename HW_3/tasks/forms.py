from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


# Поле пароль должно содержать не менее 8 символов, включая хотя бы одну букву и
# одну цифру.

# Форма должна содержать поля: имя, электронная почта,
# пароль (с подтверждением), дата рождения, согласие на
# обработку персональных данных.

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    birthdate = DateField('Birthdate', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_pas = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    consent = BooleanField('Consent to the processing of personal data', validators=[DataRequired()])