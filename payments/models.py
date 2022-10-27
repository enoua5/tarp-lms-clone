from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save

# Create your models here.
class Tuition(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=7)

    def __str__(self):
        return self.user.username

class Product(models.Model):
  product_name = models.CharField(max_length=150)
  product_type = models.CharField(max_length=25)
  product_description = models.TextField()
  product_price = models.IntegerField()


class TempProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Product)
