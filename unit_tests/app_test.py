import unittest
from requests import get
# from flask_testing import TestCase
from app import app

BASE_URL = "http://localhost:5500"

def get_file(file):
  expected_response = open(file, "r").read()
  return expected_response

class TestFlaskApp(unittest.TestCase): # change back to unittest?

  def test_login_status(self):
    url = f"{BASE_URL}/login"
    response = get(url)
    self.assertEqual(response.status_code, 200)

  def test_login_message(self):
      url = f"{BASE_URL}/login"
      response = get(url)
      expected_message =  get_file('responses/user_login.txt')
      self.assertEqual(response.text, expected_message)

  def test_mood_status(self):
    url = f"{BASE_URL}/"
    response = get(url)
    self.assertEqual(response.status_code, 200)

  def test_mood_message(self): # assert that if the connection fails, it goes to default?
      url = f"{BASE_URL}/"
      response = get(url)
      expected_message = get_file('responses/mood.txt')
      self.assertIn(expected_message, response.text)


if __name__ == "__main__":
  unittest.main()