from _config import GIPHY_API_KEY
from default import default_gifs, default_jokes, default_quotes
from random import randint
import random
import requests
from abc import ABC, abstractmethod


# This file is dedicated to classes used to make calls to the external APIs used in the app


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

    def __call__(self): # put custom try and except here and return None is unsuccessful?
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return response

    @abstractmethod
    def unpack(self):
        pass


class QuoteAPI(APIRequest):
    def __init__(self, params=None, headers=None):
        super().__init__(params, headers)
        self.url = 'https://zenquotes.io/api/today'

    def unpack(self):
        try:
            response = self.__call__()
            clean_response = response.json()
            quote = clean_response[0]['q']
            author = clean_response[0]['a']
        except Exception as e:
            print(e)
            random_quote = random.choice(list(default_quotes))
            quote = random_quote['q']
            author = random_quote['a']
        return [quote, author]

class JokeAPI(APIRequest):
    def __init__(self, params=None, headers=None):
        super().__init__(params, headers)
        self.url = 'https://icanhazdadjoke.com/'

    def unpack(self):
        try:
            response = self.__call__()
            clean_response = response.json()
            joke = clean_response['joke']
        except Exception as e:
            print(e)
            joke = random.choice(default_jokes)
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
        try:
            response = self.__call__()
            clean_response = response.json()
            list = clean_response['data']
            item = list[0]
            gif_url = item['images']['fixed_width']['mp4']
        except Exception as e:
            print(e)
            mood = self.params['q']
            gif_url = default_gifs[mood]
        return gif_url


class MoodDict(object):

    def __init__(self):
        self.dict = {}
        self.list = ['happy', 'calm', 'sad', 'worried', 'frustrated', 'angry']

    def make_dict(self):
        for mood in self.list:
            self.dict[mood] = MoodAPI(mood).unpack()
        return self.dict


