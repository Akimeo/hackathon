from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import logging
import json
from db import UsersModel

app = Flask(__name__)
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
            'login': None
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
    else:
        password = check_password(req)
        if password is None:
            res['response']['text'] = \
                'Неверный пароль! Попробуй ввести его ещё раз!'
        else:
            sessionStorage[user_id]['password'] = password
            res['response']['text'] = \
                'Молодец, ты справился!'


def check_login(req):
    login = req['request']['original_utterance']
    if UsersModel.query.filter_by(name=login).first():
        return login


def check_password(req):
    login = sessionStorage[req['session']['user_id']]['login']
    password = req['request']['original_utterance']
    user = UsersModel.query.filter_by(name=login).first()
    if user.password_hash == password:
        return password


if __name__ == '__main__':
    db.create_all()
    user = UsersModel(name='admin', password_hash='admin', donetasks='')
    db.session.add(user)
    db.session.commit()
    app.run()
