from django.db import models

# Create your models here.
class RegistUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

class WeatherData(models.Model):

    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    dt = models.CharField(max_length=32)
    min_temp = models.CharField(max_length=32)
    max_temp = models.CharField(max_length=32)
    weather = models.CharField(max_length=32)
    wind = models.CharField(max_length=32)
