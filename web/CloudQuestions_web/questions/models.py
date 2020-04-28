from django.db import models


# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=200)
    created = models.DateTimeField()
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.topic}- {self.question}\n{self.answer} '
