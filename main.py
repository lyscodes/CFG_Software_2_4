import requests
from config import key
import json
from urllib import parse, request
from random import randint

endpoint1 = 'https://zenquotes.io/api/today'


def get_moods(mood):
    url = "http://api.giphy.com/v1/gifs/search"
    offset = randint(0, 4999) # this means a new result will show up each time the call is made
    params = parse.urlencode({
        "q": mood, # set up to take input of call for mood
        "api_key": key, # key in config file
        "limit": "1", # returns on one result
        "offset": offset
    })
    try:
        with request.urlopen("".join((url, "?", params))) as response:
            data = json.loads(response.read())
            list = data['data']
            item = list[0]
            gif_url = item['url']
            print(gif_url)
            return gif_url
    except Exception:
        print("Opps: error")



def get_quote_otd():
    result = requests.get(endpoint1).json()
    quote = result[0]['q']
    author = result[0]['a']
    print(quote, author)
    return [quote, author]


"""
# this endpoint returns a list of dictionaries with author as key and quote as value
# its not being used currently but could be in future. You can uncomment and run if curious (results in terminal)

endpoint2 = 'https://zenquotes.io/api/quotes/keywords'

def get_quotes_by_keyword():
    result = requests.get(endpoint2).json()
    quotes_list = []
    for i in range(len(result)):
        quotes_list.append({result[i]['a']: result[i]['q']})
    print(quotes_list)
    return quotes_list

get_quotes_by_keyword()
"""




if __name__ == '__main__':
     mood = "sad"
     get_moods(mood)