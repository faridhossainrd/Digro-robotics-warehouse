from django.db import models
from django.utils import timezone
# Create your models here.
class Allroducts(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='pics')
    Desc = models.TextField()
    Price = models.IntegerField()
    Container = models.CharField(max_length=200)
    Box = models.IntegerField()
    Percentage =  models.IntegerField()
    Quantity = models.IntegerField()
    Date = models.DateTimeField(default=timezone.now)

class orders_storage(models.Model):
      order =  models.JSONField()
      
class Total(models.Model):
      Items = models.IntegerField()
      Products = models.IntegerField()
      Amount = models.IntegerField()
      order_complete = models.IntegerField()
      order_pending = models.IntegerField()
      order_processing = models.IntegerField()
      Sells_amount = models.IntegerField()
      containter = models.IntegerField()

class robot_map(models.Model):
       map = models.JSONField()

class productdata(models.Model):
      product_data = models.JSONField()
      Image = models.ImageField(upload_to = 'product_image')

class productupdate(models.Model):
      product_data = models.JSONField()

      
      

       