from flask import Flask, render_template, session, redirect, make_response,\
    jsonify, request
from forms import LoginForm, RegForm
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from DB import TasksModel, UsersModel, app, db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os
from sqlalchemy import exists


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def tasks():
    if 'username' not in session:
        return redirect('/login')
    user_name = session['username']
    return render_template('feed.html', username=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    form = LoginForm()
    user_name = form.username.data
    password = form.password.data
    user = db.session.query(UsersModel).filter_by(name=user_name).first()
    existence = ''
    if user:
        if check_password_hash(user.password_hash, password):
            session['username'] = user_name
            session['user_id'] = user.id
            return redirect("/")
        else:
            existence = 'Wrong password'
    elif not (user_name is None and password is None):
        existence = 'This user does not exist'
    return render_template('login.html', form=form, existence=existence)

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    user_name = form.username.data
    password = form.password.data
    password2 = form.password2.data
    existence = ''
    user = db.session.query(UsersModel).filter_by(name=user_name).first()
    if form.validate_on_submit():
        if user:
            existence = 'This name is taken'
        elif password != password2:
            existence = 'Passwords do not match'
        else:
            user = UsersModel(name=user_name, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return render_template('registration.html', form=form, existence=existence)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'username' not in session:
        return redirect('/login')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
