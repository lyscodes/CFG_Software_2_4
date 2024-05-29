from helper import get_quote_otd, get_quote_by_mood, make_moods_dict, get_joke, choice_joke_quote, submit_entry
from db_utils import today_emotion
from flask import Flask, render_template, request, flash, redirect, abort
from config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# Choose how you feel
@app.route('/', methods=['GET', 'POST'])
def mood_checkin():
    if request.method == 'GET':
        emotions = make_moods_dict()
        return render_template("mood.html", emotions=emotions)


# Accessed after choosing a feeling - allows user to choose between getting a joke or a quote
@app.route('/choice/<id>', methods=['GET', 'POST'])
def choice(id):
    if request.method == 'GET':
        today_emotion(id) # save their emotional choice to the database
        return render_template("choice.html", emotion=id)


# Get the quote of the day
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


# Save a journal entry
@app.route('/journal', methods=['GET', 'POST'])
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


# Get a joke
@app.route('/joke', methods=['GET'])
def joke_generator():
    result = get_joke()
    return render_template("joke.html", joke=result)


# Get calendar view of your entries + stats of moods
@app.route('/overview', methods=['GET'])
def show_overview():
    return render_template("overview.html")


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # to do: save the user data in db
        return redirect('/')    # seems like good practice to use redirect for POST request (for more info: https://stackoverflow.com/questions/21668481/difference-between-render-template-and-redirect)


# Log in with credentials
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # to do: implement login logic to check user credentials and save session
        return redirect('/')


# Log out user
@app.route('/logout')
def user_logout():
    # to do: clear user session
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True, port=5500)

