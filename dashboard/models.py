from django.db import models
from django.conf import settings

from course_management.models import Assignment, Course

# Create your models here.

class Notification(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    notified_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_note = models.CharField(max_length=25)

    def value_from_object(self):
        return "hi :)"