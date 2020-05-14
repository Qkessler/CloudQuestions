from django.conf import settings
from datetime import datetime
from django.db import models


class Topic(models.Model):
    topic_name = models.TextField(unique=True, db_index=True),
    created = models.DateField(default=datetime.now)


class Question(models.Model):
    created = models.DateField(default=datetime.now)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    question = models.TextField(unique=True, db_index=True)
    answer = models.TextField(unique=True, db_index=True)


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateField(default=datetime.now)
    rating = models.TextField(db_index=True)
