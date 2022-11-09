import datetime
from .models import Profile

# Django Imports
from django.test import TestCase
from django.test import Client
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Webdriver Imports
from webdriver_manager.chrome import ChromeDriverManager


# Create your tests here.
class UserEditProfileSuccessTest(TestCase):
    # Set up for the run
    user = None
    c = Client()

    def setUp(self):
        user = User.objects.create_user('testuser', 'test@gmail.com', 'asdfasdfasdf')
        Profile.objects.create(user=user)

        # attempt to log in
        success = self.c.login(username='testuser', password='asdfasdfasdf')
        self.assertTrue(success, msg='Error: Login failed.')

    def test_edit_profile(self):
        # set up input data
        input = {
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is the bio',
            'address_line1': '111 N 1111 E',
            'city': 'Layton',
            'state': 'UT',
            'zip': '84040',
            'birthdate': '2001-01-01',
            'link1': 'https://google.com',
        }

        # attempt to post
        response = self.c.post('/account/editprofile/', input)

        # Status code should be 302 for redirect
        self.assertTrue(response.status_code == 302, msg='Error: Post failed to return redirection status.')

        # get objects
        user = User.objects.get(username='testuser')
        user_profile = Profile.objects.get(user=user)

        # run assertions
        self.assertEqual(user.first_name, 'Test', msg='Error: The user\'s first name does not match.')
        self.assertEqual(user.last_name, 'User', msg='Error: The user\'s last name does not match.')
        self.assertEqual(user_profile.bio, 'This is the bio', msg='Error: The bio does not match.')
        self.assertEqual(user_profile.address_line1, '111 N 1111 E', msg='Error: Address line 1 does not match.')
        self.assertEqual(user_profile.city, 'Layton', msg='Error: The city does not match.')
        self.assertEqual(user_profile.state, 'UT', msg='Error: The state does not match.')
        self.assertEqual(user_profile.zip, '84040', msg='Error: The zip does not match.')
        self.assertEqual(user_profile.birthdate, datetime.date(2001, 1, 1), msg='Error: The birthdate does not match.')
        self.assertEqual(user_profile.link1, 'https://google.com', msg='Error: Link 1 does not match.')
        self.assertEqual(user_profile.link2, None, msg='Error: Link 2 should be none.')

    # Clean up after the test
    def tearDown(self):
        # Place code here you want to run after the test
        pass



class EditProfile(TestCase):
    theUser = None
    profile = None
    c = Client()

    # Set up for the test
    def setUp(self):
        # Create a test student
        theUser = User.objects.create_user('Locutus', 'Locutus@cube.net', 'asdfasdfasdf')
        profile = Profile(user=theUser, bio='Biography', address_line1='12345', address_line2='12345', city='Belgrade',
                          state='Serbia', zip='84025', link1='https://memory-alpha.fandom.com/wiki/Locutus_of_Borg',
                          link2='https://memory-alpha.fandom.com/wiki/Locutus_of_Borg',
                          link3='https://memory-alpha.fandom.com/wiki/Locutus_of_Borg')
        profile.save()
        response = self.c.login(username='Locutus', password='asdfasdfasdf')
        self.assertTrue(response)

    # Test that a user can edit their profile
    def test_badprofile(self):
        # Check that user can get to the profile page.
        response = self.c.get('/account/profile/')

        # Test that response is success
        self.assertTrue(response.status_code == 200, msg='Error: Failed to retrieve profile page.')

        # Check that we can get to the edit profile page.
        response = self.c.get('/account/editprofile/')

        # Test that response is success
        self.assertTrue(response.status_code == 200, msg='Error: Failed to retrieve edit page.')

        # Edit the profile with bad values
        response = self.c.post('/account/editprofile/', {'birthdate': '46254.7',
                                                         'zip': '1234567891011',
                                                         'link1': 'A Bad URL',
                                                         'link2': 'Another Bad URL',
                                                         'link3': 'A Third Bad URL'})

        # It shouldn't redirect but it should stay on the same page.
        self.assertTrue(response.status_code == 200, msg='Error: The post accepted bad values.')


    def tearDown(self):
        pass


'''
    Selenium tests
'''
class UserEditProfileSeleniumTest(LiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service)
        self.selenium.implicitly_wait(10)
        # create groups and required objects
        Group.objects.create(name='Student')
        Group.objects.create(name='Instructor')

        user = User.objects.create_user(username='testuser',  first_name='Test', last_name='User', password='asdfasdfasdf')
        Profile.objects.create(user=user, birthdate=datetime.date(2001, 1, 1))

        self.selenium.maximize_window()

    def test_edit_profile(self):
        selenium = self.selenium
        # first we need to log user in
        selenium.get('%s%s' % (self.live_server_url, '/login/'))

        # Get the elements to log in
        username_field = selenium.find_element(By.ID, 'username')
        password_field = selenium.find_element(By.ID, 'password')
        login_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Log In']")

        # Populate the form with user input.
        username_field.send_keys('testuser')
        password_field.send_keys('asdfasdfasdf')

        # Click login
        login_btn.click()

        # go to profile url
        selenium.get('%s%s' % (self.live_server_url, '/account/editprofile/'))

        # get elements for form input
        bio_field = selenium.find_element(By.ID, 'bio')
        address1_field = selenium.find_element(By.ID, 'address_line1')
        address2_field = selenium.find_element(By.ID, 'address_line2')
        city_field = selenium.find_element(By.ID, 'city')
        state_field = selenium.find_element(By.ID, 'state')
        zip_field = selenium.find_element(By.ID, 'zip')
        link1_field = selenium.find_element(By.ID, 'link1')

        # populate form
        bio_field.send_keys('This is the bio')
        address1_field.send_keys('111 N 1111 E')
        address2_field.send_keys('apt 1')
        city_field.send_keys('Layton')
        state_field.send_keys('UT')
        zip_field.send_keys('84040')
        link1_field.send_keys('https://google.com')

        # scroll down, click button
        selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        selenium.implicitly_wait(1000)
        submit_btn = selenium.find_element(By.XPATH, "//button[@type='submit']")
        # for some reason this click works while .click() doesn't???
        selenium.execute_script("arguments[0].click();", submit_btn)

        # run assertions
        user = User.objects.filter(username='testuser')[0]
        user_profile = Profile.objects.get(user=user)

        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user_profile.bio == 'This is the bio'
        assert user_profile.address_line1 == '111 N 1111 E'
        assert user_profile.address_line2 == 'apt 1'
        assert user_profile.city == 'Layton'
        assert user_profile.state == 'UT'
        assert user_profile.zip == '84040'
        assert user_profile.birthdate == datetime.date(2001, 1, 1)
        assert user_profile.link1, 'https://google.com'
        assert user_profile.link2 == ''

