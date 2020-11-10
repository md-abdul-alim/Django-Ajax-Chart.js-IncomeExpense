import django
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from six import u
# Create your models here.


class Income(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=256)
    description = models.TextField()
    amount = models.FloatField()
    date = models.DateField(default=now)

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']


class Source(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
