from flask import Flask, render_template, request
from main import get_quote_otd, make_moods_dict
# from db_utils import 

app = Flask(__name__)


@app.route('/mood', methods=['GET', 'POST'])
def mood_checkin():
    if request.method == 'GET':
        emotions = make_moods_dict()
        return render_template("mood.html", emotions=emotions)
    else:
        print("you have clicked on one of the options")


@app.route('/quote')
def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=f'Quote of the day is: {quote} By {author}')


@app.route('/journal')
def add_journal_entry():
    return render_template("journal.html")









if __name__ == '__main__':
    app.run(debug=True, port=5500)