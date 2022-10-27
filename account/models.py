from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_images/default_profile.png', upload_to='profile_images')
    bio = models.TextField(max_length=3000, default=None, null=True)
    birthdate = models.DateField(default=django.utils.timezone.now)
    address_line1 = models.CharField(max_length=200, default=None, null=True)
    address_line2 = models.CharField(max_length=200, default=None, null=True)
    city = models.CharField(max_length=100, default=None, null=True)
    state = models.CharField(max_length=50, default=None, null=True)
    zip = models.CharField(max_length=10, default=None, null=True)
    link1 = models.URLField(max_length=200, default=None, null=True)
    link2 = models.URLField(max_length=200, default=None, null=True)
    link3 = models.URLField(max_length=200, default=None, null=True)

    def __str__(self):
        return self.user.username
