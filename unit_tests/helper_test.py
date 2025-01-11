from app.helper import QuoteAPI, JokeAPI, MoodDict, MoodAPI
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

class quoteAPI(TestCase):
    @patch('apis.helper.QuoteAPI.__call__')
    def test_verify_client(self, mock_get_value: MagicMock) -> None:
        mock_get_value.return_value = 'client'
        response = QuoteAPI().__call__()
        self.assertTrue(response)

    @patch('apis.helper.QuoteAPI.__call__')
    def test_request_response(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 200
        result = QuoteAPI().__call__()
        self.assertEqual(result, 200)

    @patch('apis.helper.QuoteAPI.__call__')
    def test_request_response_bad(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 500
        result = QuoteAPI().__call__()
        self.assertEqual(result, 500)

class jokeAPI(TestCase):

    @patch('apis.helper.JokeAPI.__call__')
    def test_verify_client(self, mock_get_value: MagicMock) -> None:
        mock_get_value.return_value = 'client'
        response = JokeAPI().__call__()
        self.assertTrue(response)

    @patch('apis.helper.JokeAPI.__call__')
    def test_request_response(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 200
        result = JokeAPI().__call__()
        self.assertEqual(result, 200)

    @patch('apis.helper.JokeAPI.__call__')
    def test_request_response_bad(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 500
        result = JokeAPI().__call__()
        self.assertEqual(result, 500)


class gifAPI(TestCase):

    @patch('apis.helper.MoodAPI.__call__')
    def test_verify_client(self, mock_get_value: MagicMock) -> None:
        mock_get_value.return_value = 'client'
        response = MoodAPI('mood').__call__()
        self.assertTrue(response)

    @patch('apis.helper.MoodAPI.__call__')
    def test_request_response(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 200
        result = MoodAPI('mood').__call__()
        self.assertEqual(result, 200)

    @patch('apis.helper.MoodAPI.__call__')
    def test_request_response_bad(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 500
        result = MoodAPI('mood').__call__()
        self.assertEqual(result, 500)

class moodDict(TestCase):
    def check_dict(self):
        obj = MoodDict.make_dict()
        self.assertIsInstance(obj, dict)

if __name__ == "__main__":
    main()