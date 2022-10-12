from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from account.models import Profile
from course_management.models import Course
import unittest

# Create your tests here.

class TestClass(TestCase):
    # Set up for the run
    def setUp(self):
        # Place code here you want to run before the test.
        pass

    # Test add class
    def test_addclass(self):
        # Create a test user
        user = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        Profile.user = user
        c = Client()

        # Login the user
        success = c.login(username='testprofessor', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

        # Create the course
        response = c.post('/courses/addCourse/', {'department': 'CS',
                                                  'course_num': 4000,
                                                  'course_name': 'Test course',
                                                  'meeting_days': 'T,Th',
                                                  'meeting_start_time': '12:00',
                                                  'meeting_end_time': '12:30',
                                                  'meeting_location': 'Building 100',
                                                  'credit_hours': 4})

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        course_list = Course.objects.filter(instructor=user)

        # Check if the course was created
        self.assertEqual(course_list[0].course_num, 4000, msg='Error: Failed to create a course.')

        pass

    # Clean up after the test
    def tearDown(selfself):
        # Place code here you want to run after the test
        pass

if __name__ == '__main__':
    unittest.main()