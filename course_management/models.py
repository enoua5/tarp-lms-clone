from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator # Integer validators.
from django.conf import settings # Used for linking to user model
from multiselectfield import MultiSelectField # Used for picking multiple days.

# List of days that can be chosen for a class.
COURSE_DAYS = ((1, "M"),
               (2, "T"),
               (3, "W"),
               (4, "Th"),
               (5, "F"))


class Course(models.Model):
    department = models.CharField(max_length=4)
    course_num = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    meeting_days = MultiSelectField(choices=COURSE_DAYS, min_choices=1)
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()
    meeting_location = models.CharField(max_length=25, default="TBA")
    credit_hours = models.PositiveSmallIntegerField(default=1)