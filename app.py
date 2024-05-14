from flask import Flask, render_template
from main import get_quote_otd
# from db_utils import 

app = Flask(__name__)


@app.route('/mood')
def mood_checkin():
    my_mood = 'happy'
    return render_template("mood.html", mood=my_mood)


@app.route('/quote')
def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=f'Quote of the day is: {quote} By {author}')









if __name__ == '__main__':
    app.run(debug=True, port=5500)