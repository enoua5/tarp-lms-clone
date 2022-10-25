# Django Imports
from django.test import TestCase
from django.test import LiveServerTestCase

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

'''!
    @brief Test suite for the Login form.
    @details Allows the developer to verify that a user is able to log in.
'''
class LoginFormTest(LiveServerTestCase):
        
    def test_loginform(self):
        selenium = webdriver.Firefox()
        #Choose your url to visit
        selenium.get('http://localhost:8000/login/?next=/dashboard/')

        #find the elements you need to submit form
        username_field = selenium.find_element(By.ID, 'username')
        password_field = selenium.find_element(By.ID, 'password')
        login_btn = selenium.find_element(By.XPATH, "//input[@type='submit'][@value='Log In']")

        #populate the form with data
        username_field.send_keys('professor')
        password_field.send_keys('asdfasdfasdf')

        #submit form
        login_btn.click()

        #check result; page source looks at entire html document
        assert 'Professor Bean' in selenium.page_source