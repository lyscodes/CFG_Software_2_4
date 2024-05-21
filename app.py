from flask import Flask, render_template, request
from main import get_quote_otd, get_quote_by_mood, get_moods, get_joke
# from db_utils import 

app = Flask(__name__)


@app.route('/mood', methods=['GET', 'POST'])
def mood_checkin():
    if request.method == 'GET':
        return render_template("mood.html")
    else:
        print("you have clicked on one of the options")


@app.route('/quote', methods=['GET'])
def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=f'Quote of the day is: {quote} By {author}')


# This is hardcoded to happiness to limit api calls
@app.route('/quote/keyword', methods=['GET'])
def quote_for_mood():
    result = get_quote_by_mood()
    quote = result[0]
    author = result[1]
    return (f'Your quote based on your selected mood is: {quote} By {author}')


'''
# use this instead of hard coded function when ready to go live:

@app.route('/quote/<mood>', methods=['GET'])
def quote_for_mood(mood):
    result = get_quote_by_mood(mood)
    quote = result[0]
    author = result[1]
    return (f'Your quote based on your selected mood is: {quote} By {author}')
'''


@app.route('/joke', methods=['GET'])
def joke_generator():
    result = get_joke()
    return result






if __name__ == '__main__':
    app.run(debug=True, port=5500)