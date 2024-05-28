from config import GIPHY_API_KEY
from default import default_gifs
from random import randint
import requests
from abc import ABC, abstractmethod


class APIRequest(ABC):
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

    @abstractmethod
    def unpack(self):
        pass


class QuoteAPI(APIRequest):
    def __init__(self, params=None, headers=None):
        super().__init__(params, headers)
        self.url = 'https://zenquotes.io/api/today'

    def unpack(self):
        response = self.__call__()
        quote = response[0]['q']
        author = response[0]['a']
        return [quote, author]

class JokeAPI(APIRequest):
    def __init__(self, params=None, headers=None):
        super().__init__(params, headers)
        self.url = 'https://icanhazdadjoke.com/'

    def unpack(self):
        response = self.__call__()
        joke = response['joke']
        return joke


class MoodAPI(APIRequest):
    def __init__(self, mood, headers=None):
        super().__init__(headers)
        self.url = "http://api.giphy.com/v1/gifs/search"
        self.params = {"q": mood,
            "api_key": GIPHY_API_KEY,
            "limit": "1",
            "offset": randint(0, 300)}

    def unpack(self):
        response = self.__call__()
        list = response['data']
        item = list[0]
        gif_url = item['images']['fixed_width']['mp4']
        return gif_url


class MoodDict(object):

    def __init__(self):
        self.dict = {}
        self.list = ['happy', 'calm', 'sad', 'worried', 'frustrated', 'angry']

    def make_dict(self):
        for mood in self.list:
            gif_url = MoodAPI(mood).unpack()
            if gif_url:
                self.dict[mood] = gif_url
            else:
                self.dict[mood] = default_gifs[mood]
        return self.dict


# tests of API endpoints

getquote = QuoteAPI()
print(getquote.unpack())

getjoke = JokeAPI()
print(getjoke.unpack())

mood_dict = MoodDict().make_dict()

print(mood_dict)