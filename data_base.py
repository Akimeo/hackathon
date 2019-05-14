from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UnderTask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TasksModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(1000), unique=True, nullable=False)
    author = db.Column(db.Integer, unique=False, nullable=False)
    user = db.Column(db.Integer, unique=False, default=0)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    priority = db.Column(db.Integer, unique=False, nullable=False, default=1)
    done_date = db.Column(db.DateTime, unique=False, nullable=True)
    phase = db.Column(db.Integer, unique=False, nullable=False, default=0)
    deleg_user = db.Column(db.ARRAY, unique=False, nullable=False, default=[])


class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    alice_id = db.Column(db.String(), unique=False, default=0)
    tg_id = db.Column(db.Integer, unique=False, default=0)


db.create_all()
