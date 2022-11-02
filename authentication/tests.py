import os
# Django Imports
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Webdriver Imports
from webdriver_manager.chrome import ChromeDriverManager

'''!
    @brief Test suite for the Login form.
    @details Allows the developer to verify that a user is able to log in.
'''
class LoginFormTest(LiveServerTestCase):
    '''!
        @brief The below will install the correct browser driver (default to Chrome)
            for our UI tests.
    '''
    service = Service(executable_path=ChromeDriverManager().install())

    def test_loginform(self):
        selenium = webdriver.Chrome(service=self.service)
        # Give Selenium the URL to go to.
        selenium.get('http://localhost:8000/login/?next=/dashboard/')

        # Get the elements that we'll be interacting with.
        username_field = selenium.find_element(By.ID, 'username')
        password_field = selenium.find_element(By.ID, 'password')
        login_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Log In']")

        # Populate the form with user input.
        username_field.send_keys('professor')
        password_field.send_keys('asdfasdfasdf')

        # Click login
        login_btn.click()

        # Check that we were redirected to the dashboard
        assert 'dashboard' in selenium.current_url


'''!
    @brief Test suite for the Signup form.
    @details Allows the developer to verify that a user is able to create an account.
'''
class SignupFormTest(LiveServerTestCase):
    '''!
        @brief The below will install the correct browser driver (default to Chrome)
            for our UI tests.
    '''
    service = Service(executable_path=ChromeDriverManager().install())


    def setUp(self):
        self.selenium = webdriver.Chrome(service=self.service)
        self.selenium.implicitly_wait(10)
    #
    # def tearDown(self):
    #     self.selenium.quit()

    def test_signupform(self):
        selenium = self.selenium
        # Give Selenium the URL to go to.
        selenium.get('%s%s' % (self.live_server_url, '/login/signup/'))

        # Get the elements that we'll be interacting with.
        username_field = selenium.find_element(By.ID, 'username')
        email_field = selenium.find_element(By.ID, 'email')
        fname_field = selenium.find_element(By.ID, 'first_name')
        lname_field = selenium.find_element(By.ID, 'last_name')
        birthdate_field = selenium.find_element(By.ID, 'birthdate')
        password1_field = selenium.find_element(By.ID, 'password1')
        password2_field = selenium.find_element(By.ID, 'password2')
        # no need for account field, the default is student

        signup_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Sign Up']")

        # Populate the form with user input
        username_field.send_keys('testuser')
        email_field.send_keys('testuser@gmail.com')
        fname_field.send_keys('Test')
        lname_field.send_keys('User')
        birthdate_field.send_keys('01/01/2001')
        password1_field.send_keys('asdfasdfasdf')
        password2_field.send_keys('asdfasdfasdf')

        self.selenium.implicitly_wait(100)

        # Click signup
        #signup_btn.click()

        # Check that we were redirected to the dashboard
        #assert 'dashboard' in selenium.current_url

        # Check that the user was created
        #new_user = User.objects.filter(username='testuser').first()
        a#ssert new_user.username == 'testuser'
