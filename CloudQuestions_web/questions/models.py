from django_sorcery.db import databases
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User as auth_user
from sqlalchemy.orm import mapper


db = databases.get('default')


class User(object):
    def __init__(self, id, password, last_login, is_superuser,
                 username, first_name, email, is_staff, is_active,
                 date_joined, last_name):
        self.id = id
        self.password = password
        self.last_login = last_login
        self.is_superuser = is_superuser
        self.username = username
        self.first_name = first_name
        self.email = email
        self.is_staff = is_staff
        self.is_active = is_active
        self.date_joined = date_joined
        self.last_name = last_name

        
mapper(User, auth_user)


class Topic(db.Model):
    __tablename__ = 'Topic'

    id = db.Column(db.Integer(), primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(), unique=True)
    created = db.Column(db.DateTime,
                        default=datetime.now, nullable=False)


class Question(db.Model):
    __tablename__ = 'Question'

    id = db.Column(db.Integer(), primary_key=True,
                   autoincrement=True, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now,
                        nullable=False)
    topic = db.Column(db.Integer(),
                      db.ForeignKey(Topic.id), nullable=False)
    question = db.Column(db.String(), unique=True)
    answer = db.Column(db.String())


class Rating(db.Model):
    id = db.Column(db.Integer(), primary_key=True,
                   autoincrement=True, nullable=False)
    user = db.Column(db.ForeignKey(User.id), nullable=False, index=True)
    topic = db.Column(db.Integer(),
                      db.ForeignKey(Topic.id), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now,
                        nullable=False)
    rating = db.Column(db.String(), nullable=False)
