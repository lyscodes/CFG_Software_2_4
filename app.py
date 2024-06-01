from db_utils import today_emotion, add_new_user, check_email, check_username, verify_cred
from flask import Flask, render_template, request, flash, redirect, session
from config import SECRET_KEY
from helper_oop import QuoteAPI, JokeAPI, MoodDict
from registration_form import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Choose how you feel
@app.route('/', methods=['GET', 'POST'])
def mood_checkin():
    if request.method == 'GET':
        emotions = MoodDict().make_dict()
        return render_template("mood.html", emotions=emotions)


# Accessed after choosing a feeling - allows user to choose between getting a joke or a quote
@app.route('/choice/<id>', methods=['GET', 'POST'])
def choice(id):
    if request.method == 'GET':
        today_emotion(id)
        return render_template("choice.html", emotion=id)


# Get the quote of the day
@app.route('/quote', methods=['GET'])
def quote_of_the_day():
    result = QuoteAPI().unpack()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)

'''
@app.route('/quote/keyword', methods=['GET'])
def quote_for_mood():
    result = get_quote_by_mood()
    quote = result[0]
    author = result[1]
    return render_template("quote.html", quote=quote, author=author)



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
    result = QuoteAPI().unpack()
    quote = result[0]
    author = result[1]
    if request.method == 'POST':
        content = request.form.get('textarea')
        if not content:
            flash('Journal is empty')
        else:
            response = add_journal_entry(content)
            if response == True:
                flash('Entry submitted')
            elif response == False:
                flash('You have already submitted a diary entry for this date')
    return render_template("journal.html", quote=quote, author=author)


# Get a joke
@app.route('/joke', methods=['GET'])
def joke_generator():
    result = JokeAPI().unpack()
    return render_template("joke.html", joke=result)


# Get calendar view of your entries + stats of moods
@app.route('/overview', methods=['GET'])
def show_overview():
    return render_template("overview.html")



# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        content = {}
        for item in ["FirstName", "LastName", "Username", "email", "password", "confirm", "accept_tos"]:
            content[item] = request.form.get(item)
        if content['password'] != content['confirm']:
            flash('Password and Password Confirmation do not match')
        elif check_email(content['email']):
            flash('Email already registered')
        elif check_username(content['Username']):
            flash('Username already in use')
        elif add_new_user(content):
            return redirect('/login/new_user')
        else:
            flash('We were unable to register you at this time. Please try again later')
    return render_template("register.html", form=form)


# Log in with credentials
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<new_user>', methods=['GET', 'POST'])
def user_login(new_user=""):
    if new_user == "new_user":
        flash("Success! Your  account has been created. Please login")
    if request.method == 'POST':
        session.clear()
        username = request.form.get('uname')
        password = request.form.get('password')
        if not check_username(username):
            flash("This username does not exist")
        elif verify_cred(username, password):
            session['user_name'] = username
            return redirect('/')
        elif not verify_cred(username, password):
            flash("Username and Password do not match")
        else:
            flash("Something went wrong! Please try again later")
    return render_template("login.html")

# Log out user
@app.route('/logout')
def user_logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=5500)