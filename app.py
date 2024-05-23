from flask import Flask, render_template, request
from main import get_quote_otd, get_quote_by_mood, make_moods_dict, get_joke
# from db_utils import 

app = Flask(__name__)


@app.route('/')
@app.route('/mood', methods=['GET', 'POST'])
def mood_checkin():
    if request.method == 'GET':
        emotions = make_moods_dict()
        return render_template("mood.html", emotions=emotions)
    else:
        print("you have clicked on one of the options")


@app.route('/quote', methods=['GET'])
def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)


@app.route('/quote/keyword', methods=['GET'])
def quote_for_mood():
    result = get_quote_by_mood()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)


'''
# use this instead of hard coded function when ready to go live:

@app.route('/quote/<mood>', methods=['GET'])
def quote_for_mood(mood):
    result = get_quote_by_mood(mood)
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)

'''


@app.route('/journal')
def add_journal_entry():
    result = get_quote_otd() # This is a quick solution, but we should save the data from /quote call to the api instead
    quote = result[0]
    author = result[1]
    return render_template("journal.html", quote=quote, author=author)


@app.route('/joke', methods=['GET'])
def joke_generator():
    result = get_joke()
    return render_template("joke.html", joke=result)


@app.route('/overview', methods=['GET'])
def show_overview():
    return render_template("overview.html")




if __name__ == '__main__':
    app.run(debug=True, port=5500)