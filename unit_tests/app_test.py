import unittest
from flask import url_for
from flask_testing import TestCase
from app import app

BASE_URL = "http://localhost:5500"


# using Flask's test library
class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_template_rendered_mood(self):
        response = self.client.get('/')
        self.assert_template_used('mood.html')

    def test_template_rendered_quote(self):
        response = self.client.get('/quote')
        self.assert_template_used('quote.html')

    def test_form_submission_wrongpw(self): # check password validaiton and flash messages
        response = self.client.post('/register', data={'FirstName': 'Rachel', 'LastName': 'Tookey', "Username": "Rachel1993", "email": "rachel@tookey.com", "password":"snow", "confirm":"rain", "accept_tos":True})
        self.assert_message_flashed('Password and Password Confirmation do not match', "error")

    def test_overview_redirect(self): # check it redirects if not logged in
        response = self.client.get('/overview')
        self.assert_status(response, 302, message=None)


if __name__ == "__main__":
    unittest.main()
