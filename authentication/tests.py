# Django Imports
from django.test import TestCase
from django.test import LiveServerTestCase

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

        # Check that we were redirected to the dashboard and we see "Professor Bean"
        assert 'Professor Bean' in selenium.page_source
        assert 