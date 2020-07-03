from django.conf import settings
from datetime import datetime
from django.db import models


class Topic(models.Model):
    name = models.TextField(unique=True, db_index=True, default='')
    created = models.DateField(default=datetime.now)
    color = models.IntegerField(null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.DO_NOTHING,
                                db_index=True)
    created_flag = models.BooleanField(default=True)
    privacy = models.BooleanField(default=False)


class Question(models.Model):
    created = models.DateField(default=datetime.now)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_index=True)
    question = models.TextField(unique=False, db_index=True)
    answer = models.TextField(unique=False, db_index=True)
    added_flag = models.BooleanField(default=True)


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, db_index=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateField(default=datetime.now)
    rating = models.TextField(db_index=True)


class CalendarConnection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, db_index=True)
    connection = models.BooleanField(default=False)
