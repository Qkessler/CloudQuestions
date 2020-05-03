from django.contrib.auth.models import update_last_login, user_logged_in
from django.contrib.auth import check_password, make_password
from django.contrib.auth import random_characters
from .model_base import ModelBase
import sqlalchemy

user_logged_in.disconnect(update_last_login)


class User(ModelBase):
    __tablename__ = "User"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    salt = sqlalchemy.Column(sqlalchemy.String(10))
    password = sqlalchemy.Column(sqlalchemy.String(128))

    USERNAME_FIELD = 'username'

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, password):
        if not self.salt:
            self.salt = random_characters(10)
        self.password = make_password(password, salt=self.salt)
