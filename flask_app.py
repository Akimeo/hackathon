from flask import Flask, request
import logging
import json
from data_base import UsersModel, TasksModel
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vwb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = \
            'Привет! Для авторизации в системе UnderTask введи свой логин!'
        sessionStorage[user_id] = {
            'login': None,
            'password': None
        }
        return
    if sessionStorage[user_id]['login'] is None:
        login = check_login(req)
        if login is None:
            res['response']['text'] = \
                'Пользователь не найден! Попробуй ввести логин ещё раз!'
        else:
            sessionStorage[user_id]['login'] = login
            res['response']['text'] = \
                'А теперь, ' + login + ', введи свой пароль!'
    elif sessionStorage[user_id]['password'] is None:
        password = check_password(req)
        if password is None:
            res['response']['text'] = \
                'Неверный пароль! Попробуй ввести его ещё раз!'
        else:
            sessionStorage[user_id]['password'] = password
            res['response']['text'] = \
                'Добро пожаловать в систему UnderTask!'
            res['response']['buttons'] = [
                {
                    'title': 'Покажи мои задачи',
                    'hide': True
                }
            ]
    else:
        ou = req['request']['original_utterance'].lower()
        if 'покаж' in ou and 'задач' in ou:
            res['response']['text'] = show_tasks(req)
        else:
            res['response']['text'] = \
                'Прости, я тебя не поняла!'
            res['response']['buttons'] = [
                {
                    'title': 'Покажи мои задачи',
                    'hide': True
                }
            ]


def show_tasks(req):
    ut_id = db.session.query(UsersModel).filter_by(
        alice_id=req['session']['user_id']).first().id
    tasks = db.session.query(TasksModel).filter_by(author=ut_id).all()
    ans = ''
    for task in tasks:
        ans += 'Название: ' + task.name + '\nid: ' + \
            str(task.id) + '\nДата выполнения: ' + str(task.date) + '\n\n'
    if ans:
        return ans
    else:
        return 'Пока здесь пусто!'


def check_login(req):
    login = req['request']['original_utterance']
    if db.session.query(UsersModel).filter_by(name=login).first():
        return login


def check_password(req):
    login = sessionStorage[req['session']['user_id']]['login']
    password = req['request']['original_utterance']
    user = db.session.query(UsersModel).filter_by(name=login).first()
    if user.password_hash == password:
        user.alice_id = req['session']['user_id']
        db.session.commit()
        return password


def find_id(req):
    user_id = req['session']['user_id']
    user = db.session.query(UsersModel).filter_by(alice_id=user_id).first()
    return user.id


if __name__ == '__main__':
    db.create_all()
    app.run()
