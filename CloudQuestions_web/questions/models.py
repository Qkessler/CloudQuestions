from django_sorcery.db import databases
from datetime import datetime
# from django.contrib.auth.models import update_last_login, user_logged_in
# from django.contrib.auth import check_password, make_password
# from django.contrib.auth import random_characters


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


# user_logged_in.disconnect(update_last_login)


# class User(db.Model):
#     __tablename__ = "User"

#     id = db.Column(db.Integer(), primary_key=True)
#     username = db.Column(db.String(), unique=True)
#     salt = db.Column(db.String(length=10))
#     password = db.Column(db.String(legth=128))

#     USERNAME_FIELD = 'username'

#     def is_authenticated(self):
#         return True

#     def is_anonymous(self):
#         return False

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     def set_password(self, password):
#         if not self.salt:
#             self.salt = random_characters(10)
#         self.password = make_password(password, salt=self.salt)
