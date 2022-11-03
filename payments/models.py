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
