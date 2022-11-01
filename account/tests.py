import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from .models import Profile


# Create your tests here.
class UserEditProfileTest(TestCase):
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
