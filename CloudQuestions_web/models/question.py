import sqlalchemy
from datetime import datetime
from models.model_base import ModelBase
from .topic import Topic


class Question(ModelBase):
    __tablename__ = 'Question'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False)
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now,
                                nullable=False)
    topic = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey(Topic.id),
                              nullable=False)
    question = sqlalchemy.Column(sqlalchemy.String, unique=True)
    answer = sqlalchemy.Column(sqlalchemy.String)
