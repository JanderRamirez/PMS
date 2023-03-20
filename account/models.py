from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    f_name = models.CharField(max_length=50)
    m_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    type = models.IntegerField()
    status = models.IntegerField()
    profile = models.CharField(max_length=255)