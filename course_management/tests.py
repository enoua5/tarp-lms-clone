from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from account.models import Profile
from course_management.models import Course, Assignment, TextSubmission
import unittest

from payments.models import Tuition

# Create your tests here.

class TestMakeCourse(TestCase):
    # Set up for the run
    user = None
    c = Client()
    def setUp(self):
        # Create a test user
        user = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        Profile.user = user

        # Login the user
        success = self.c.login(username='testprofessor', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

    # Test add class
    def test_addclass(self):

        # Create the course
        response = self.c.post('/courses/addCourse/', {'department': 'CS',
                                                  'course_num': 4000,
                                                  'course_name': 'Test course',
                                                  'meeting_days': 'T,Th',
                                                  'meeting_start_time': '12:00',
                                                  'meeting_end_time': '12:30',
                                                  'meeting_location': 'Building 100',
                                                  'credit_hours': 4})

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        course_list = Course.objects.filter(course_num=4000)

        # Check if the course was created
        self.assertEqual(course_list[0].course_num, 4000, msg='Error: Failed to create a course.')

    # Clean up after the test
    def tearDown(selfself):
        # Place code here you want to run after the test
        pass

class StudentCanRegisterForCourseTest(TestCase):
        self.user = User.objects.create_user('registering_student', 'student@stu.dent', 'asdfasdfasdf')
        Tuition.objects.create(user=self.user)
        professor = User.objects.create_user('professor_test', 'test@pro.fessor', 'asdfasdfasdf')
        Course.objects.create(department='THING', course_num=2210, course_name='Testing things',
                              instructor=professor, meeting_days='M,T,W', meeting_start_time='12:00',
                              meeting_end_time='1:00', meeting_location='where ever, lol', credit_hours=3)

        Profile.user = self.user

        # Login the user
        success = self.c.login(username='registering_student', password='asdfasdfasdf')
        
    def test_student_register(self):
        # get objects created in setup
        course = Course.objects.filter(department='THING', course_num=2210).first()

        # create url for registration
        url = '/courses/registration/register/' + str(course.id)

        # register for the course
        response = self.c.post(url)

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status. Instead returned '+str(response.status_code))

        print(course in self.user.courses.all())

        # Check if the student is in the course
        self.assertTrue(course in self.user.courses.all(), msg='Error: Failed to register for course.')

    # Clean up after the test
    def tearDown(self):
        # Place code here you want to run after the test
        pass
        
class StudentSubmitTextAssignmentTest(TestCase):
    # Set up for the run
    user = None
    c = Client()
    def setUp(self):
        # Create test objects
        user = User.objects.create_user('teststudent', 'student@gmail.com', 'asdfasdfasdf')
        professor = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        course = Course.objects.create(department='CS', course_num=4000, course_name='Test course',
                                       instructor=professor, meeting_days='T,Th', meeting_start_time='12:00',
                                       meeting_end_time='12:30', meeting_location='Building 100', credit_hours=4)
        assignment = Assignment.objects.create(course=course, title='Test Assignment',
                                               description='This is the test assignment',
                                               due_date='2022-12-31 23:59:00', points=100, type='t')

        Profile.user = user

        # Login the user
        success = self.c.login(username='teststudent', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

    # Test add class
    def test_student_submit_text_assignment(self):

        # get objects created in setup
        user = User.objects.filter(username='teststudent').first()
        course = Course.objects.filter(course_num=4000).first()
        assignment = Assignment.objects.filter(title='Test Assignment').first()

        # create url for submission post
        url = '/courses/' + str(course.id) + '/' + str(assignment.id)

        # Create the submission
        response = self.c.post(url, {'text': 'This is the test text submission'})

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        submissions = TextSubmission.objects.filter(student=user, assignment=assignment)

        # Check if the course was created
        self.assertEqual(submissions[0].text, 'This is the test text submission', msg='Error: Failed to create submission.')

    # Clean up after the test
    def tearDown(self):
        # Place code here you want to run after the test
        pass
        
if __name__ == '__main__':
    unittest.main()
