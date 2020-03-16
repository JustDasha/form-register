from flask import Flask, render_template, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import users, db_session

import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    hashed_password = StringField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    speciality = StringField('Профессия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class LoginForm(FlaskForm):
    id_user = StringField('id астронавта', validators=[DataRequired()])
    password_user = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_cap = StringField('id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.hashed_password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            surname=form.surname.data,
            address=form.address.data,
            position=form.address.data,
            hashed_password=form.hashed_password.data,
            age=form.age.data,
            email=form.email.data,
            speciality=form.speciality.data
        )

        user.set_password(form.hashed_password.data)
        session.add(user)
        session.commit()
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init(input())
    app.run(port=8080, host='127.0.0.1')
