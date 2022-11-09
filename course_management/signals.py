from django.db.models.signals import post_save
from django.dispatch import receiver

from course_management.models import Assignment, Submission
from dashboard.models import Notification

@receiver(post_save, sender=Assignment)
def assignment_created(sender, instance, created, **kwargs):
    if created:
        note = "created"
    else:
        note = "updated"

    for student in instance.course.students.all():
        Notification(
            course=instance.course,
            assignment=instance,
            notified_user=student,
            event_note = note
        ).save()

# Checking for a changed field required doing the grade update check in the model's save() method
@receiver(post_save, sender=Submission)
def submission_changed(sender, instance, created, **kwargs):
    if created:
        Notification(
            course=instance.assignment.course,
            assignment=instance.assignment,
            notified_user=instance.student,
            event_note = "new submission"
        ).save()
