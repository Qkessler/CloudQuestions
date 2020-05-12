from django_sorcery.db import databases
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User as auth_user


db = databases.get('default')


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
    #TODO: needs changing.
    user = db.Column(db.Integer(), nullable=False, index=True)
    topic = db.Column(db.Integer(),
                      db.ForeignKey(Topic.id), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now,
                        nullable=False)
    rating = db.Column(db.String(), nullable=False)
