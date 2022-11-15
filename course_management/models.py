from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator # Integer validators.
from django.contrib.auth.models import User
from django.conf import settings # Used for linking to user model
import datetime, pytz # Time & timezone abilities
import os


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
    a_threshold = models.PositiveSmallIntegerField(default=93)
    increment = models.PositiveSmallIntegerField(default=4)
    
    def __str__(self):
        return self.department + " " + str(self.course_num) + " " + self.course_name
        
    '''!
        @brief Returns the "short" course name of the current course.
        @details Returns a string in the format "XX 0000".
    '''
    def getShortCourseName(self):
        return f"{self.department} {self.course_num}"
        
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
    
    '''!
        @brief Calculates the student's grade, letter and percent, for the current course.
        @param in_student Student object (typically the user).
        @return student_grade A Python dictionary of the format {'letter': str, 'percent': float}
    '''
    def getStudentGrade(self, in_student):
        # Collect graded submissions for the student
        assignment_list = Assignment.objects.filter(course=self)
        student_grade = {'letter': 'N/A',
                        'percent': -1.0}
        scored_points = 0
        total_points = 0
        
        for assignment in assignment_list:
            studentSubmissions = Submission.objects.filter(assignment_id=assignment.id, student_id=in_student.id)
            gradedSubmissions = list(filter(lambda submission: submission.score is not None, studentSubmissions))
            if len(gradedSubmissions) != 0:
                # Sorting to get only the last graded submission.
                gradedSubmissions.sort(key=lambda submission: submission.submitted_at, reverse=True)
                scored_points += gradedSubmissions[0].score
                total_points += assignment.points
                
        if total_points != 0:
            student_grade['percent'] = round((scored_points / total_points) * 100.0, 2)
            student_grade['letter'] = self.calcLetterGrade(student_grade['percent'])
            
        return student_grade 

    '''!
        @brief Calculates the letter grade that a student currently has in the course.
        @param percentGrade The student's current grade percent in the course.
    '''
    def calcLetterGrade(self, percentGrade):
        # Cut out the A threshold
        Ascore = self.a_threshold
        # Cut out the increment value
        inc = self.increment
        letterGrade = None

        if (percentGrade >= Ascore):
            letterGrade = 'A'
        elif (percentGrade >= (Ascore - inc)):
            letterGrade = 'A-'
        elif (percentGrade >= (Ascore - (inc * 2))):
            letterGrade = 'B+'
        elif (percentGrade >= (Ascore - (inc * 3))):
            letterGrade = 'B'
        elif (percentGrade >= (Ascore - (inc * 4))):
            letterGrade = 'B-'
        elif (percentGrade >= (Ascore - (inc * 5))):
            letterGrade = 'C+'
        elif (percentGrade >= (Ascore - (inc * 6))):
            letterGrade = 'C'
        elif (percentGrade >= (Ascore - (inc * 7))):
            letterGrade = 'C-'
        elif (percentGrade >= (Ascore - (inc * 8))):
            letterGrade = 'D+'
        elif (percentGrade >= (Ascore - (inc * 9))):
            letterGrade = 'D'
        elif (percentGrade >= (Ascore - (inc * 10))):
            letterGrade = 'D-'
        else:
            letterGrade = 'E'

        return letterGrade


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
        @return True if the assignment is overdue; False otherwise.
    '''
    def overdue(self):
        universalTimeZone = pytz.UTC
        now = universalTimeZone.localize(datetime.datetime.now())
        if self.due_date <= now:
            return True
        return False
        
    '''!
        @brief Returns a user-friendly string that indicates when the assignment is due.
        @return due_date_string A string of the format "Today at 11:59PM" or "05/29 at 10:40PM"
    '''
    def getUserFriendlyDueDate(self):
        due_date_string = ""

        today = datetime.datetime.now().day
        assignment_due_day = self.due_date.day
        
        # Check if assignment is due today or tomorrow.
        if (today == assignment_due_day):
            due_date_string += "Today"
        elif ((today+1) == assignment_due_day):
            due_date_string += "Tomorrow"
        else:
            due_date_string += f"{self.due_date.strftime('%m/%d/%Y')}"
            
        due_date_string += f" at {self.due_date.strftime('%I:%M%p')}"
        
        return due_date_string  

# submission models
class Submission(models.Model):
    score = models.PositiveIntegerField(null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    __prev_score = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__prev_score = self.score

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.score != self.__prev_score:
            from dashboard.models import Notification
            # assignment grade changed!
            if self.__prev_score == None:
                note = "graded"
            else:
                note = "grade changed"
            Notification(
                course=self.assignment.course,
                assignment=self.assignment,
                notified_user=self.student,
                event_note = note
            ).save()
        super().save(force_insert, force_update, *args, **kwargs)
        self.__prev_score = self.score


class FileSubmission(Submission):
    # file will save to MEDIA_ROOT/submissions/<assignment.id>/<student.id>/<filename>
    def get_submission_path(self, filename):
        return os.path.join(
            'submissions',
            str(self.assignment.id),
            str(self.student.id),
            filename,
        )
    file = models.FileField(upload_to=get_submission_path)


class TextSubmission(Submission):
    text = models.TextField(max_length=30000)
