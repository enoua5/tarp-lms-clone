from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator # Integer validators.
from django.conf import settings # Used for linking to user model
import datetime
from django.forms.widgets import NumberInput

class Course(models.Model):
    department = models.CharField(max_length=20)
    course_num = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)])
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    meeting_days = models.TextField()
    meeting_start_time = models.TimeField(default='12:00')
    meeting_end_time = models.TimeField(default='12:00')
    meeting_location = models.CharField(max_length=25)
    credit_hours = models.PositiveSmallIntegerField(default=3)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses")
    
    def __str__(self):
        return self.department + " " + str(self.course_num) + " " + self.course_name
        
        
    '''!
        @brief Formats the course's meeting days and returns a string in the format
               D, D, D.
    '''
    def getFormattedCourseDays(self):
        DAY_OF_WEEK_CHOICES = [
        ("M", "Monday"),
        ("T", "Tuesday"),
        ("W", "Wednesday"),
        ("Th", "Thursday"),
        ("F", "Friday"),
        ]
        # Removing brackets
        courseDays = self.meeting_days.replace('[', '')
        courseDays = courseDays.replace(']', '')
        # Removing apostrophes
        courseDays = courseDays.replace("'", '')
        # Condensing day names into their abbreviations
        for weekday in DAY_OF_WEEK_CHOICES:
            courseDays = courseDays.replace(str(weekday[1]), str(weekday[0]))
            
        return courseDays


# assignment model
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    due_date = models.DateTimeField()
    points = models.PositiveIntegerField()
    type = models.CharField(max_length=1, choices=(('t', 'Text entry'), ('f', 'File upload')))

    def __str__(self):
        return self.title
    
    '''!
        @brief Returns whether or not the current assignment is overdue.
    '''
    def overdue(self):
        now = datetime.datetime.now()
        if self.due_date < now:
            return True
        
    '''!
        @brief Returns a user-friendly string that indicates when the assignment is due.
        @return due_date_string A string of the format "Today at 11:59PM" or "05/29 at 10:40PM"
    '''
    def getUserFriendlyDueDate(self):
        due_date_string = ""

        today = datetime.datetime.now().date.day
        assignment_due_day = self.due_date.date.day
        
        # Check if assignment is due today or tomorrow.
        if (today == assignment_due_day):
            due_date_string += "Today"
        elif ((today+1) == assignment_due_day):
            due_date_string += "Tomorrow"
        else:
            due_date_string += f"{self.due_date.strftime('%m/%d')}"
            
        due_date_string += f" at {self.due_date.strftime('%I:%M%p')}"
        
        return due_date_string  
