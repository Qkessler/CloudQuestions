from datetime import datetime
import sqlalchemy
from models.model_base import ModelBase


class Topic(ModelBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    topic = sqlalchemy.Column(sqlalchemy.String)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.now, nullable=False)
    question = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False, unique=True)
    answer = sqlalchemy.Column(sqlalchemy.String,
                               nullable=False, unique=True)
