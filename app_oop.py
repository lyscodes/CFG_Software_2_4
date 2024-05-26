from flask import Flask, render_template, request, flash, make_response
from helper import get_quote_otd, get_quote_by_mood, make_moods_dict, get_joke, choice_joke_quote, submit_entry
from config import SECRET_KEY

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
        emotions = make_moods_dict()
        return render_template("mood.html", emotions=emotions)

def choice(id):
    if request.method == 'GET':
        choice_joke_quote(id)
        return render_template("choice.html", emotion=id)


def quote_of_the_day():
    result = get_quote_otd()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)


def quote_for_mood():
    result = get_quote_by_mood()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)


def add_journal_entry():
    result = get_quote_otd() # This is a quick solution, but we should save the data from /quote call to the api instead
    quote = result[0]
    author = result[1]
    if request.method == 'POST':
        content = request.form.get('textarea')
        if not content:
            flash('Journal is empty')
        else:
            response = submit_entry(content)
            if response == True:
                flash('Entry submitted')
                # use fetch here to dynamically take away the form? With an offer to visit overview?
            elif response == False:
                flash('You have already submitted a diary entry for this date')
    return render_template("journal.html", quote=quote, author=author)

def joke_generator():
    result = get_joke()
    return render_template("joke.html", joke=result)

def show_overview():
    return render_template("overview.html")


app.add_endpoint('/', 'mood_checkin', mood_checkin, methods=['GET', 'POST'])
app.add_endpoint('/choice/<id>', 'choice', choice, methods=['GET', 'POST'])
app.add_endpoint('/quote', 'quote_of_the_day', quote_of_the_day, methods=['GET'])
app.add_endpoint('/quote/keyword', 'quote_for_mood', quote_for_mood, methods=['GET'])
app.add_endpoint('/journal', 'journal', add_journal_entry, methods=['GET', 'POST'])
app.add_endpoint('/joke', 'joke', joke_generator, methods=['GET'])
app.add_endpoint('/overview', 'overview', show_overview, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True, port=5500)