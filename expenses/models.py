import django
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from six import u
# Create your models here.


class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    description = models.TextField()
    amount = models.FloatField()
    date = models.DateField(default=now)
    
    

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        # this name will show in admin table.
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
