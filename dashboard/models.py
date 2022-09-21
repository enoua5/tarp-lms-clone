from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Course(models.Model):
    department = models.CharField(max_length=4)
    coursenum = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    coursename = models.CharField(max_length=100)
    instname = models.CharField(max_length=20)
    meetingtime = models.CharField(max_length=25)