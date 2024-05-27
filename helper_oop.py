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


class QuoteAPI(APIRequest):
    def __init__(self, url, params=None, headers=None):
        super().__init__(url, params, headers)

    def unpack(self):
        response = self.__call__()
        quote = response[0]['q']
        author = response[0]['a']
        return [quote, author]

class JokeAPI(APIRequest):
    def __init__(self, url, params=None, headers=None):
        super().__init__(url, params, headers)

    def unpack(self):
        response = self.__call__()
        joke = response['joke']
        return joke


class MoodAPI(APIRequest):
    def __init__(self, url, params=None, headers=None):
        super().__init__(url, params, headers)

    def unpack(self):
        response = self.__call__()
        list = response['data']
        item = list[0]
        gif_url = item['images']['fixed_width']['mp4']
        return gif_url

    def make_mood_dict(self, list):
        moods_dict = {}

        for mood in list:
            self.params['q'] = mood
            self.params["offset"] = randint(0, 300)
            gif_url = self.unpack()
            if gif_url:
                moods_dict[mood] = gif_url
            else:
                moods_dict[mood] = default_gifs[mood]
        return moods_dict



url_quote = 'https://zenquotes.io/api/today'
getquote = QuoteAPI(url_quote)
print(getquote.unpack())


url_joke = 'https://icanhazdadjoke.com/'
getjoke = JokeAPI(url_joke)
print(getjoke.unpack())

url = "http://api.giphy.com/v1/gifs/search"
params = {
        "q": "happy",
        "api_key": GIPHY_API_KEY,
        "limit": "1",
        "offset": 1
    }

getmood = MoodAPI(url, params=params, headers=None)
main_moods = ['happy', 'calm', 'sad', 'worried', 'frustrated', 'angry']
mood_dict = getmood.make_mood_dict(main_moods)

print(mood_dict)



