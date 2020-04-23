from datetime import datetime
import sqlalchemy
from models.model_base import ModelBase


class Topic(ModelBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.datetime.now, index=True)
    question = sqlalchemy.Column(sqlalchemy.String, index=True)
    answer = sqlalchemy.Column(sqlalchemy.String, index=True)
