from flask import Flask
from main import get_quote_otd
# from db_utils import 

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return f'Quote of the day is: {quote} By {author}'







if __name__ == '__main__':
    app.run(debug=True, port=5500)