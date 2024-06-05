import unittest
from requests import get

BASE_URL = "http://localhost:5000"

class TestFlaskApp(unittest.TestCase):

  def test_mood_endpoint(self):
    url = f"{BASE_URL}/"

    # Send a GET request to the endpoint
    response = get(url)

    # Assert that the request was successful
    self.assertEqual(response.status_code, 200)

    # Assert the response content
    expected_message = "Hello from Flask!"
    self.assertEqual(response.text, expected_message)

if __name__ == "__main__":
  unittest.main()