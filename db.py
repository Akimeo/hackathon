from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vwb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TasksModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(1000), unique=True, nullable=False)
    author = db.Column(db.Integer, unique=False, nullable=False)
    user = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    phase = db.Column(db.Integer, unique=False, nullable=False, default=0)


class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    donetasks = db.Column(db.String(), unique=False,
                          nullable=True, default='[]')
    alice_id = db.Column(db.Integer, unique=True, default=0)
    tg_id = db.Column(db.Integer, unique=True, default=0)
