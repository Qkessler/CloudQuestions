from datetime import datetime
import sqlalchemy
from models.model_base import ModelBase


# Creating table Topic(id, topic, created, question, answer).
class Topic(ModelBase):
    __tablename__ = 'Topic'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime,
                                default=datetime.now, nullable=False)
