from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Course(models.Model):
    department = models.CharField(max_length=4)
    course_num = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    course_name = models.CharField(max_length=100)
    inst_name = models.CharField(max_length=20)
    meeting_time = models.CharField(max_length=25)
    meeting_location = models.CharField(max_length=25,default="Online")