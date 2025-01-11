import unittest
from flask_testing import TestCase
from app import app

# Testing file for routes.py and Flask ending points. It uses flask's customised library for testing.

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.secret_key = 'test_key'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_template_rendered(self):
        self.client.get('/')
        self.assert_template_used('mood.html')

    def test_template_rendered_quote(self):
        self.client.get('/quote')
        self.assert_template_used('quote.html')

    def test_template_rendered_choice(self):
        with self.client:
            with self.client.session_transaction() as test_sess:
                test_sess['mood_dict'] = {'sad': ''}
            self.client.get('/choice/sad')
            self.assert_template_used('choice.html')

    def test_template_rendered_joke(self):
        self.client.get('/joke')
        self.assert_template_used('joke.html')

    def test_template_rendered_journal(self):
        self.client.get('/journal')
        self.assert_template_used('journal.html')

    def test_overview_redirect(self): # check it redirects if not logged in
        response = self.client.get('/overview', follow_redirects=False)
        self.assert_status(response, 302)

    def test_form_submission_wrongpw(self): # check password validaiton and flash messages
        self.client.post('/register', data={'FirstName': 'Rachel', 'LastName': 'Tookey', "Username": "Rachel1993", "email": "rachel@tookey.com", "password":"snow", "confirm":"rain", "accept_tos":True})
        self.assert_message_flashed('Password and Password Confirmation do not match', "error")

    def test_username_taken(self): # check password validaiton and flash messages
        self.client.post('/register', data={'FirstName': 'Rachel', 'LastName': 'Tookey', "Username": "JoDoe", "email": "r@tookey.com", "password":"snow", "confirm":"snow", "accept_tos":True})
        self.assert_message_flashed("Username already in use", "error")


    def test_form(self): # check it redirects if not logged in
        response = self.client.post('/register', data={'FirstName': 'Rachel', 'LastName': 'Tookey', "Username": "Rachel1993", "email": "rachel@tookey.com", "password":"snow", "confirm":"snow", "accept_tos":True}, follow_redirects=True)
        self.assert_200(response)


    def test_404(self):
        response = self.client.get('/hello')
        self.assert404(response)

    def test_login_200(self):
        response = self.client.get('/login')
        self.assert_200(response, 200)

    def test_login_credentials_200(self):
        response = self.client.post('/login', data={'uname': 'JoDoe', 'password': 'password123'}, follow_redirects=True)
        self.assert_200(response, 200)


    def test_session(self):
        with self.client.session_transaction() as test_sess:
            test_sess['user'] = 'testuser'
        self.assertIn('user', test_sess)

    def test_login_overview(self):
        with self.client:
            with self.client.session_transaction() as session:
                session['user'] = 'testuser'
            response = self.client.get('/overview')
            self.assert200(response)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=False)
        self.assert_status(response, 302)

    def test_logout_flash(self):
        self.client.get('/logout')
        self.assert_message_flashed("You have been logged out. See you soon!", "notification")

    def test_logout_session(self):
        with self.client:
            with self.client.session_transaction() as test_sess:
                test_sess['user'] = 'testuser'
            self.client.get('/logout')
            with self.client.session_transaction() as test_sess:
                self.assertNotIn('user', test_sess)

if __name__ == "__main__":
    unittest.main()
