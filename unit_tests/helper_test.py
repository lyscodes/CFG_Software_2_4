from helper_oop import QuoteAPI, JokeAPI, MoodDict, MoodAPI
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

class quoteAPI(TestCase):
    @patch('helper_oop.QuoteAPI.__call__')
    def test_verify_client(self, mock_get_value: MagicMock) -> None:
        mock_get_value.return_value = 'client'
        response = QuoteAPI().__call__()
        self.assertTrue(response)

    @patch('helper_oop.QuoteAPI.__call__')
    def test_request_response(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 200
        result = QuoteAPI().__call__()
        self.assertEqual(result, 200)

    @patch('helper_oop.QuoteAPI.__call__')
    def test_request_response_bad(self, mock_response: MagicMock) -> None:
        mock_response.return_value = 500
        result = QuoteAPI().__call__()
        self.assertEqual(result, 500)

class jokeAPI(TestCase):
    pass

if __name__ == "__main__":
    main()