import requests
import json


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