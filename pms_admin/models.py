from django.db import models
from django.utils.timezone import now
# Create your models here.

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    gen_name = models.CharField(max_length=100)
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    s_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10)
    category = models.IntegerField()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=now)
    staff = models.IntegerField()

class Sales_details(models.Model):
    id = models.AutoField(primary_key=True)
    sales_id = models.IntegerField()
    med_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
