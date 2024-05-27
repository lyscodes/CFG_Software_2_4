from config import GIPHY_API_KEY
from default import default_gifs
from random import randint
import requests


class APIRequest(object):
    def __init__(self, url, params=None, headers=None):
        self.url = url

        if headers is not None:
            self.headers = headers
        else:
            self.headers = {'accept':'application/json'}

        if params is not None:
            self.params = params
        else:
            self.params = {}

    def __call__(self):
        response = requests.get(self.url, params=self.params, headers=self.headers).json()
        return response


class MoodAPI(APIRequest):
    def __init__(self, url, params=None, headers=None):
        super().__init__(url, params, headers)

    def __call__(self):
        response = requests.get(self.url, params=self.params, headers=self.headers).json()
        return response

    def make_mood_dict(self, list):
        moods_dict = {}

        for mood in list:
            self.params['q'] = mood
            gif_url = self.__call__()
            if gif_url:
                moods_dict[mood] = gif_url
            else:
                moods_dict[mood] = default_gifs[mood]
        return moods_dict



url_quote = 'https://zenquotes.io/api/today'
getquote = APIRequest(url_quote)
print(getquote.__call__())


url_joke = 'https://icanhazdadjoke.com/'
getjoke = APIRequest(url_joke)
print(getjoke.__call__())

url = "http://api.giphy.com/v1/gifs/search"
params = {
        "q": "happy",
        "api_key": GIPHY_API_KEY,
        "limit": "1",
        "offset": 1
    }
getmood = MoodAPI(url, params=params, headers=None)
print(getmood.__call__())
main_moods = ['happy', 'calm', 'sad', 'worried', 'frustrated', 'angry']

mood_dict = getmood.make_mood_dict(main_moods)

print(mood_dict)



