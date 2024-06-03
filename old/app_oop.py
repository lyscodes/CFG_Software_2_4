from flask import Flask, render_template, request, flash, make_response
from config import SECRET_KEY
from helper_oop import QuoteAPI, JokeAPI, MoodDict
from db_utils import today_emotion, add_journal_entry
import datetime

date = datetime.datetime.now().date()


class EndpointHandler(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        response = self.action(*args, **request.view_args)
        return make_response(response)


class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, *configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointHandler(handler), methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)


flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
key = ('SECRET_KEY', SECRET_KEY)
app.configs(key)

def mood_checkin():
    if request.method == 'GET':
        emotions = MoodDict()
        emotions_list = emotions.make_dict()
        return render_template("mood.html", emotions=emotions_list)

def choice(id):
    if request.method == 'GET':
        return render_template("choice.html", emotion=id)


def quote_of_the_day():
    result = QuoteAPI().unpack()
    return render_template("quote.html", quote=result[0], author=result[1])


def add_journal_entry():
    result = QuoteAPI().unpack()
    if request.method == 'POST':
        content = request.form.get('textarea')
        if not content:
            flash('Journal is empty')
        else:
            response = add_journal_entry(content, date)
            if response == True:
                flash('Entry submitted')
                # use fetch here to dynamically take away the form? With an offer to visit overview?
            elif response == False:
                flash('You have already submitted a diary entry for this date')
    return render_template("journal.html", quote=result[0], author=result[1])

def joke_generator():
    result = JokeAPI().unpack()
    return render_template("joke.html", joke=result)

def show_overview():
    return render_template("overview.html")


app.add_endpoint('/', 'mood_checkin', mood_checkin, methods=['GET', 'POST'])
app.add_endpoint('/choice/<id>', 'choice', choice, methods=['GET', 'POST'])
app.add_endpoint('/quote', 'quote_of_the_day', quote_of_the_day, methods=['GET'])
app.add_endpoint('/journal', 'journal', add_journal_entry, methods=['GET', 'POST'])
app.add_endpoint('/joke', 'joke', joke_generator, methods=['GET'])
app.add_endpoint('/overview', 'overview', show_overview, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True, port=5500)