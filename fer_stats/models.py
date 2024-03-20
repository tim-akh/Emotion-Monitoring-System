from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Emotion(models.Model):
    name = models.CharField(max_length=12, default='')


class Record(models.Model):
    date_time = models.DateTimeField()
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)