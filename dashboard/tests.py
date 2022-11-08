from datetime import datetime
from time import sleep

from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import User, Group

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from dashboard.models import Notification
from course_management.models import Assignment, Course

# Create your tests here.

class NotificationRecievedTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service)
        # create test user
        self.user = User.objects.create_user('seleniumNotificationTestUser', password='asdfasdfasdf')
        # create groups to avoid crash
        Group.objects.create(name='Student')
        Group.objects.create(name='Instructor')
        self.client = Client()
        self.client.login(username='seleniumNotificationTestUser', password='asdfasdfasdf')
        self.instructor = User.objects.create_user('seleniumNotificationTestInstructpr', password='asdfasdfasdf')

        self.course = Course.objects.create(department="TEST", course_num="2210", course_name="testing selenium", instructor=self.instructor, meeting_days="MWF", meeting_location="wherever")
        self.course.students.set([self.user])
        self.assignment = Assignment.objects.create(course=self.course, title="testing notifications", description="", due_date=datetime.now(), points=100, type='t')

        self.selenium.maximize_window()

    def test_notification_recieve(self):
        # needs some fenagling to actually login without doing it on the forms
        selenium = self.selenium
        cookie = self.client.cookies['sessionid']
        selenium.get(self.live_server_url)
        selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        selenium.refresh()
        selenium.get(self.live_server_url)


        bell_icon = selenium.find_element(By.ID, 'notification-icon')
        assert "no-notif" in bell_icon.get_attribute("class")

        # create the notification
        self.notif = Notification.objects.create(notified_user = self.user, course=self.course, assignment=self.assignment)

        sleep(15)

        assert "yes-notif" in bell_icon.get_attribute("class")

    def tearDown(self):
        self.notif.delete()
        self.assignment.delete()
        self.course.delete()
        self.user.delete()
        self.instructor.delete()

