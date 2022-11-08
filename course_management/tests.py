from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.test import Client
from account.models import Profile
from course_management.models import Course, Assignment, Submission, TextSubmission, Assignment
import unittest
from django.test import LiveServerTestCase
# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# Webdriver Imports
from webdriver_manager.chrome import ChromeDriverManager
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
                                                  'credit_hours': 4,
                                                  # Had to add those since the model has changed
                                                  'a_threshold':93,
                                                  'increment':4})

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
    # Set up for the run
    user = None
    c = Client()
    def setUp(self):
        self.user = User.objects.create_user('registering_student', 'student@stu.dent', 'asdfasdfasdf')
        Tuition.objects.create(user=self.user)
        professor = User.objects.create_user('professor_test', 'test@pro.fessor', 'asdfasdfasdf')
        Course.objects.create(department='THING', course_num=2210, course_name='Testing things',
                              instructor=professor, meeting_days='M,T,W', meeting_start_time='12:00',
                              meeting_end_time='1:00', meeting_location='where ever, lol', credit_hours=3, a_threshold=93, increment=4)

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
                                       meeting_end_time='12:30', meeting_location='Building 100', credit_hours=4, a_threshold=93, increment=4)
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
        url = '/courses/' + str(course.id) + '/' + str(assignment.id) + '/submit'

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

class CreateAssignmentTest(TestCase):
    # Set up for the run
    user = None
    c = Client()
    def setUp(self):
        # Create a test user
        user = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        course = Course.objects.create(department='CS', course_num=4000, course_name='Test course',
                                        instructor=user, meeting_days='T,Th', meeting_start_time='12:00',
                                        meeting_end_time='12:30', meeting_location='Building 100', credit_hours=4, a_threshold=93, increment=4)
        Profile.user = user

        # Login the user
        success = self.c.login(username='testprofessor', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

    # Test add class
    def test_create_assignment(self):
        # get objects created in setup
        course = Course.objects.filter(course_num=4000).first()

        # create url for submission post
        url = '/courses/' + str(course.id) + '/addAssignment'

        # Create the course
        response = self.c.post('/courses/addCourse/', {'department': 'CS',
                                                  'course_num': 4000,
                                                  'course_name': 'Test course',
                                                  'meeting_days': 'T,Th',
                                                  'meeting_start_time': '12:00',
                                                  'meeting_end_time': '12:30',
                                                  'meeting_location': 'Building 100',
                                                  'credit_hours': 4})
        # Create the submission
        response = self.c.post(url, {'title': 'UnitTestAssign', 
                                    'description': 'Test Description',
                                    'due_date': '2022-05-05T23:50',
                                    'points': 100,
                                    'type': 't'})

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        assignments_list = Assignment.objects.filter(title='UnitTestAssign')

        # Check if the course was created
        self.assertEqual(assignments_list[0].title, 'UnitTestAssign', msg='Error: Failed to create an assignment.')

    # Clean up after the test
    def tearDown(selfself):
        # Place code here you want to run after the test
        pass

class PollCourseListTest(TestCase):
    user = None
    c = Client()
    def setUp(self):
        # Create a test user
        user = User.objects.create_user('testprofessor1', 'prof1@gmail.com', 'asdfasdfasdf')
        Profile.user = user

        # Login the user
        success = self.c.login(username='testprofessor1', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

        # Create a course
        Course(
            department= 'CS',
            course_num= 4000,
            course_name= 'Test course',
            meeting_days= 'T,Th',
            meeting_start_time= '12:00',
            meeting_end_time= '12:30',
            meeting_location= 'Building 100',
            credit_hours= 4,
            instructor = user
        ).save()
        # Create another test user
        user = User.objects.create_user('testprofessor2', 'prof2@gmail.com', 'asdfasdfasdf')
        Profile.user = user

        # Login the user
        success = self.c.login(username='testprofessor2', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')
        # Create another course
        Course(
            department= 'CS',
            course_num= 4001,
            course_name= 'Another test course',
            meeting_days= 'T,Th',
            meeting_start_time= '12:00',
            meeting_end_time= '12:30',
            meeting_location= 'Building 101',
            credit_hours= 4,
            instructor = user
        ).save()

        # Create yet another test user
        user = User.objects.create_user('teststudent1', 'stud1@gmail.com', 'asdfasdfasdf')
        Profile.user = user
        user.user_permissions.add(Permission.objects.get(name="Can view course"))

        # Login the user
        success = self.c.login(username='teststudent1', password='asdfasdfasdf')

        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

        
    def test_poll_courses(self):
        response = self.c.get('/data/?command=get_all&item_type=course')
        courses = response.json()['items']

        self.assertEqual(len(courses), 2)
        self.assertTrue(
            courses[0]['course_num'] == 4000 and courses[1]['course_num'] == 4001
            or
            courses[0]['course_num'] == 4001 and courses[1]['course_num'] == 4000
        )

    def tearDown(self):
        pass

class GradeAssignmentTest(TestCase):
    # Set up for the run
    user = None
    c = Client()
    def setUp(self):
        # Create test objects
        student = User.objects.create_user('teststudent', 'student@gmail.com', 'asdfasdfasdf')
        professor = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        course = Course.objects.create(department='CS', course_num=4000, course_name='Test course',
                                       instructor=professor, meeting_days='T,Th', meeting_start_time='12:00',
                                       meeting_end_time='12:30', meeting_location='Building 100', credit_hours=4, a_threshold=93, increment=4)
        assignment = Assignment.objects.create(course=course, title='UnitTestAssign',
                                               description='This is the test assignment',
                                               due_date='2022-12-31 23:59:00', points=100, type='t')
        submission = TextSubmission.objects.create(text='Unit test', assignment_id=assignment.id, student_id=student.id)
        # Login the user
        success = self.c.login(username='testprofessor', password='asdfasdfasdf')
        
        # Check if login was successful
        self.assertTrue(success, msg='Error: Login failed.')

    # Test add class
    def test_grade_assignment(self):
        # get objects created in setup
        course = Course.objects.filter(course_num=4000).first()
        assignment = Assignment.objects.filter(title='UnitTestAssign')[0]
        submission = TextSubmission.objects.filter(text='Unit test')[0]

        assignments_list = Assignment.objects.filter(title='UnitTestAssign')
        # Check if the assignment was created
        self.assertEqual(assignments_list[0].title, 'UnitTestAssign', msg='Error: Failed to create an assignment.')

        # create url for submission post
        url = '/courses/grade/' + str(submission.id)

        # # Create the submission
        response = self.c.post(url, {'score':30})

        # # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        # Testing if the grade applied
        full_submission = Submission.objects.get(id=submission.id)
        self.assertTrue(full_submission.score == 30, msg='Error: Submission failed to be graded.')

    # Clean up after the test
    def tearDown(selfself):
        # Place code here you want to run after the test
        pass

'''
    Selenium tests
'''
class SubmitAssignmentTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service)
        self.selenium.maximize_window()

        # Creating necessary objects
        user = User.objects.create_user('teststudent', 'student@gmail.com', 'asdfasdfasdf')
        professor = User.objects.create_user('testprofessor', 'prof@gmail.com', 'asdfasdfasdf')
        course = Course.objects.create(department='CS', course_num=4000, course_name='Test course',
                                       instructor=professor, meeting_days='T,Th', meeting_start_time='12:00',
                                       meeting_end_time='12:30', meeting_location='Building 100', credit_hours=4, a_threshold=93, increment=4)
        assignment = Assignment.objects.create(course=course, title='Test Assignment',
                                               description='This is the test assignment',
                                               due_date='2022-12-31 23:59:00', points=100, type='t')
    def test_submitsuccessform(self):
        selenium = self.selenium
        # Give Selenium the URL to go to.
        selenium.get('%s%s' % (self.live_server_url, '/login/'))

        # Finding the necessary objects
        course = Course.objects.filter(course_name='Test course')[0]
        assignment = Assignment.objects.filter(title='Test Assignment')[0]
        user = User.objects.filter(username='teststudent')[0]

        # Get the elements that we'll be interacting with.
        username_field = selenium.find_element(By.ID, 'username')
        password_field = selenium.find_element(By.ID, 'password')
        login_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Log In']")

        # Populate the form with user input.
        username_field.send_keys('teststudent')
        password_field.send_keys('asdfasdfasdf')

        # Click login
        login_btn.click()

        # Check that we were redirected to the dashboard
        # assert 'dashboard' in selenium.current_url

        # Go to a correct submission page
        # IMPORTANT: assumes that the pages are not protected
        url = '/courses/' + str(course.id) + '/' + str(assignment.id) + '/submit'
        selenium.get('%s%s' % (self.live_server_url, url))

        # Get the input field and the button
        input_field = selenium.find_element(By.ID, 'id_text')
        button = selenium.find_element(By.XPATH, "//button[contains(text(),'Submit')]")

        # Put the data into a form
        input_field.send_keys('Seleium test submission')
        button.click()
        
        assert 'courses/' + str(course.id) in selenium.current_url

        # Making sure the submission is there
        submission = TextSubmission.objects.filter(text='Seleium test submission')
        assert submission.count() > 0

        # Making sure the submission is connected with a right user
        submission = Submission.objects.filter(student=user.id)
        assert submission.count() > 0

class TestCalendarLink(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service)
        self.selenium.maximize_window()
        selenium = self.selenium

        user = User.objects.create_user('NoonienSoong', 'NSoong@gmail.com', 'asdfasdfasdf')



    def test_link(self):
        selenium = self.selenium
        # Give Selenium the URL to go to.
        selenium.get('%s%s' % (self.live_server_url, '/login/'))


        # Login the user
        uname = selenium.find_element(By.ID, 'username')
        pword = selenium.find_element(By.ID, 'password')
        login_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Log In']")

        uname.send_keys('NoonienSoong')
        pword.send_keys('asdfasdfasdf')

        login_btn.click()

        assert selenium.current_url == (self.live_server_url + '/dashboard/')

        # Go to the calendar
        calendar_btn = selenium.find_element(By.XPATH, "//a[contains(text(),'Calendar')]")
        calendar_btn.click()

        # Check that we made it to the calendar
        assert selenium.current_url == (self.live_server_url + '/calendars/')

        next_btn = selenium.find_element(By.XPATH, "//button[@title='Next month']")

        # Make sure we can go through all the months
        i = 0
        while i < 12:
            next_btn.click()
            i = i + 1

        # Go back to the dashboard
        btn = selenium.find_element(By.XPATH, "//a[contains(text(),'Dashboard')]")
        btn.click()

        assert selenium.current_url == (self.live_server_url + '/dashboard/')

        # Logout
        btn = selenium.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
        btn.click()

        # Check that logout was successful
        assert selenium.current_url == (self.live_server_url + '/login/')


    def tearDown(self):
        pass