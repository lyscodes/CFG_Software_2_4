import requests
from config import GIPHY_API_KEY, MOOD_API_KEY
from default import default_gifs
from urllib import parse, request
from random import randint
from db_utils import today_emotion, add_journal_entry
import datetime
import json
import random



def get_moods(mood):
    url = "http://api.giphy.com/v1/gifs/search"
    offset = randint(0, 300) # this means a new result will show up each time the call is made
    params = parse.urlencode({
        "q": mood, # set up to take input of call for mood
        "api_key": GIPHY_API_KEY, # key in config file
        "limit": "1", # returns on one result
        "offset": offset
    })
    try:
        with request.urlopen("".join((url, "?", params))) as response:
            data = json.loads(response.read())
            list = data['data']
            item = list[0]
            gif_url = item['images']['fixed_width']['mp4'] # this is the url needed to embed the gif
            return gif_url
    except Exception:
        print("Opps: error")
        return None



def make_moods_dict():
    main_moods = ['happy' , 'calm', 'sad', 'worried', 'frustrated', 'angry']
    moods_dict = {}

    # check if session has expired (if not use available data)
    
    for mood in main_moods:
        gif_url = get_moods(mood)
        # If the api calls doesn't work for any of the gifs, the default gif will show instead
        if gif_url:
            moods_dict[mood] = gif_url
        else:
            moods_dict[mood] = default_gifs[mood]
    return moods_dict


def choice_joke_quote(id):
    date = datetime.datetime.now().date()
    today_emotion(id, date)  # save their emotional choice to the database


def get_joke():
    result = requests.get('https://icanhazdadjoke.com/', headers={'accept': 'application/json'}).json()
    joke = result['joke']
    return joke


def get_quote_otd():
    result = requests.get('https://zenquotes.io/api/today').json()
    quote = result[0]['q']
    author = result[0]['a']
    return [quote, author]


# the api we are using only get 28 free calls a month...
# I think that is fine for this project but to limit api calls I have created a hardcoded list in a to not waste calls whilst we build
# The format is exactly the same as the real api result :)

def get_quote_by_mood():
    hard_code_list = [{'quote': 'The Paradoxical CommandmentsPeople are illogical, unreasonable, and self-centered. Love them anyway. If you do good, people will accuse you of selfish ulterior motives. Do good anyway. If you are successful, you will win false friends and true enemies. Succeed anyway. The good you do today will be forgotten tomorrow. Do good anyway. Honesty and frankness make you vulnerable. Be honest and frank anyway. The biggest men and women with the biggest ideas can be shot down by the smallest men and women with the smallest minds. Think big anyway. People favor underdogs but follow only top dogs. Fight for a few underdogs anyway. What you spend years building may be destroyed overnight. Build anyway. People really need help but may attack you if you do help them. Help people anyway. Give the world the best you have and youll get kicked in the teeth. Give the world the best you have anyway.', 'author': 'Kent M. Keith'}, {'quote': 'For every minute you are angry you lose sixty seconds of happiness.', 'author': 'Ralph Waldo Emerson'}, {'quote': 'Love is that condition in which the happiness of another person is essential to your own.', 'author': 'Robert A. Heinlein'}, {'quote': 'Folks are usually about as happy as they make their minds up to be.', 'author': 'Abraham Lincoln'}, {'quote': 'Time you enjoy wasting is not wasted time.', 'author': 'Marthe Troly-Curtin'}, {'quote': 'Its so hard to forget pain, but its even harder to remember sweetness. We have no scar to show for happiness. We learn so little from peace.', 'author': 'Chuck Palahniuk'}, {'quote': 'Happiness in intelligent people is the rarest thing I know.', 'author': 'Ernest Hemingway'}, {'quote': 'You will never be happy if you continue to search for what happiness consists of. You will never live if you are looking for the meaning of life.', 'author': 'Albert Camus'}, {'quote': 'The Seven Social Sins are: Wealth without work. Pleasure without conscience. Knowledge without character. Commerce without morality. Science without humanity. Worship without sacrifice. Politics without principle. From a sermon given by Frederick Lewis Donaldson in Westminster Abbey, London, on March 20, 1925.', 'author': 'Frederick Lewis Donaldson'}, {'quote': 'Happiness is when what you think, what you say, and what you do are in harmony.', 'author': 'Mahatma Gandhi'}, {'quote': 'Every man has his secret sorrows which the world knows not; and often times we call a man cold when he is only sad.', 'author': 'Henry Wadsworth Longfellow'}, {'quote': 'Theres nothing like deep breaths after laughing that hard. Nothing in the world like a sore stomach for the right reasons.', 'author': 'Stephen Chbosky'}, {'quote': 'Count your age by friends, not years. Count your life by smiles, not tears.', 'author': 'John Lennon'}, {'quote': 'Happiness is not something ready made. It comes from your own actions.', 'author': 'Dalai Lama XIV'}, {'quote': 'Promise YourselfTo be so strong that nothingcan disturb your peace of mind. To talk health, happiness, and prosperityto every person you meet. To make all your friends feelthat there is something in themTo look at the sunny side of everythingand make your optimism come true. To think only the best, to work only for the best,and to expect only the best. To be just as enthusiastic about the success of othersas you are about your own. To forget the mistakes of the pastand press on to the greater achievements of the future. To wear a cheerful countenance at all timesand give every living creature you meet a smile. To give so much time to the improvement of yourselfthat you have no time to criticize others. To be too large for worry, too noble for anger, too strong for fear,and too happy to permit the presence of trouble. To think well of yourself and to proclaim this fact to the world,not in loud words but great deeds. To live in faith that the whole world is on your sideso long as you are true to the best that is in you.', 'author': 'Christian D. Larson'}, {'quote': 'If more of us valued food and cheer and song above hoarded gold, it would be a merrier world.', 'author': 'J.R.R. Tolkien'}, {'quote': 'Attitude is a choice. Happiness is a choice. Optimism is a choice. Kindness is a choice. Giving is a choice. Respect is a choice. Whatever choice you make makes you. Choose wisely.', 'author': 'Roy T. Bennett'}, {'quote': 'They say a person needs just three things to be truly happy in this world: someone to love, something to do, and something to hope for.', 'author': 'Tom Bodett'}, {'quote': 'Take responsibility of your own happiness, never put it in other people’s hands.', 'author': 'Roy T. Bennett'}, {'quote': 'The most important thing is to enjoy your life—to be happy—its all that matters.', 'author': 'Audrey Hepburn'}, {'quote': 'Happiness is a warm puppy.', 'author': 'Charles M. Schulz'}, {'quote': 'You cannot protect yourself from sadness without protecting yourself from happiness.', 'author': 'Jonathan Safran Foer'}, {'quote': 'Don’t waste your time in anger, regrets, worries, and grudges. Life is too short to be unhappy.', 'author': 'Roy T. Bennett'}, {'quote': 'It isnt what you have or who you are or where you are or what you are doing that makes you happy or unhappy. It is what you think about it.', 'author': 'Dale Carnegie'}, {'quote': 'Even if you cannot change all the people around you, you can change the people you choose to be around. Life is too short to waste your time on people who don’t respect, appreciate, and value you. Spend your life with people who make you smile, laugh, and feel loved.', 'author': 'Roy T. Bennett'}, {'quote': 'No medicine cures what happiness cannot.', 'author': 'Gabriel GarcíA MáRquez'}, {'quote': 'Happiness is having a large, loving, caring, close-knit family in another city.', 'author': 'George Burns'}, {'quote': 'Let us be grateful to the people who make us happy; they are the charming gardeners who make our souls blossom.', 'author': 'Marcel Proust'}, {'quote': 'If you want to be happy, do not dwell in the past, do not worry about the future, focus on living fully in the present.', 'author': 'Roy T. Bennett'}, {'quote': 'I felt my lungs inflate with the onrush of scenery—air, mountains, trees, people. I thought, "This is what it is to be happy.', 'author': 'Sylvia Plath'}]
    random_quote = random.choice(hard_code_list)
    author = random_quote['author']
    quote = random_quote['quote']
    return [quote, author]


'''
# use this instead of hard coded function when ready to go live:

def get_quote_by_mood(mood):
    result = requests.get(f'https://mood-based-quote-api.p.rapidapi.com/{mood}', headers={'x-rapidapi-key': MOOD_API_KEY, 'X-RapidAPI-Host': 'mood-based-quote-api.p.rapidapi.com'}).json()
    result_list = result['result']
    random_quote = random.choice(result_list)
    quote = random_quote['quote']
    author = random_quote['author']
    return [quote, author]

'''


'''
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
'''

def submit_entry(entry):
    date = datetime.datetime.now().date()
    
    return add_journal_entry(entry, date)


if __name__ == '__main__':
     mood = "sad"
     get_moods(mood)