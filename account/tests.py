from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from account.models import Profile
import django

# Create your tests here.
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
        self.c.login(username='Locutus', password='asdfasdfasdf')

    # Test that a user can edit their profile
    def test_editprofile(self):
        # Check that user can get to the profile page.
        response = self.c.get('/account/profile/')

        # Test that response is success
        self.assertTrue(response.status_code == 200, msg='Error: Failed to retrieve profile page.')

        # Check that we can get to the edit profile page.
        response = self.c.get('/account/editprofile/')

        # Test that response is success
        self.assertTrue(response.status_code == 200, msg='Error: Failed to retrieve edit page.')

        # Edit the profile
        response = self.c.post('/account/editprofile/', {'bio': 'New Biography'})

        # Test that response is success
        self.assertTrue(response.status_code == 200, msg='Error: Failed to update profile.')


    def tearDown(self):
        pass