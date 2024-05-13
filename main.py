import requests
import json

from config import GIPHY_API_KEY



def get_gif():
    mood = 'happy'
    endpointGif = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={mood}&limit=1&offset=0&rating=g&lang=en&bundle=messaging_non_clips'
    how_are_you = requests.get(endpointGif).json()
    return how_are_you

endpoint1 = 'https://zenquotes.io/api/today'

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

# if __name__ == '__main__':
#     run()