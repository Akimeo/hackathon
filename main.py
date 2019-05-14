from flask import Flask, render_template, session, redirect, make_response,\
    jsonify, request
from forms import LoginForm, RegForm, AddTaskForm
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from DB import TasksModel, UsersModel, app, db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
deadlines = True


@app.route('/')
def tasks():
    if 'username' not in session:
        return redirect('/login')
    user_name = session['username']
    tasks = list(db.session.query(TasksModel))
    if deadlines:
        tasks = list(db.session.query(TasksModel))
    else:
        tasks = list(filter(lambda x: x.date < datetime.now(), tasks))
    authors = [db.session.query(UsersModel).filter_by(id=i.author).first().name
               for i in tasks]
    listy = range(len(tasks))
    users = [db.session.query(UsersModel).filter_by(id=j).first().name for j in
             [i.user for i in tasks]]
    return render_template('feed.html', username=user_name, tasks=tasks, listy=listy, id=session['user_id'],authors=authors, users=users, now=datetime.now())

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

@app.route('/edit-task/<id>', methods=['GET', 'POST'])
def add_taskid(id):
    if 'username' not in session:
        return redirect('/login')
    form = AddTaskForm()
    form.user.choices = [(i.id, i.name) for i in db.session.query(UsersModel)]
    task = db.session.query(TasksModel).filter_by(id=id).first()
    if task:
        namey = task.name
        descy = task.desc
    else:
        return redirect('/')
    name = form.name.data
    desc = form.desc.data
    priority = form.priority.data
    user = form.user.data
    date = form.date.data
    if form.validate_on_submit():
        task.name = name
        task.desc = desc
        task.priority = priority
        task.date = date
        task.user = user
        db.session.commit()
        return redirect('/')
    return render_template('add_tasks.html', username=session['username'], form=form, name=namey,desc=descy)

@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if 'username' not in session:
        return redirect('/login')
    form = AddTaskForm()
    form.user.choices = [(i.id, i.name) for i in db.session.query(UsersModel)]
    name = form.name.data
    desc = form.desc.data
    priority = form.priority.data
    user = form.user.data
    date = form.date.data
    if form.validate_on_submit():
        task = TasksModel(name=name, desc=desc, author=session['user_id'], date=date, priority=priority, user=user)
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    return render_template('add_tasks.html', username=session['username'], form=form, name='', desc='')

@app.route('/filter-on')
def filter_on():
    global deadlines
    deadlines = False
    return redirect('/')

@app.route('/filter-off')
def filter_off():
    global deadlines
    deadlines = True
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
