from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_images/default_profile.png', upload_to='profile_images')
    bio = models.CharField(max_length=3000, default='bio')
    birthdate = models.DateField(default=django.utils.timezone.now)
    address = models.CharField(max_length=200, default='address')
    link1 = models.URLField(max_length=200)
    link2 = models.URLField(max_length=200)
    link3 = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username
