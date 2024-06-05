from db_utils import get_user_id, today_emotion, add_new_user, check_email, check_username, check_entry_journal, verify_cred, check_entry, add_journal, get_records, verify_password
from flask import Flask, render_template, request, flash, redirect, session
from config import SECRET_KEY
from helper_oop import QuoteAPI, JokeAPI, MoodDict
from registration_form import RegistrationForm
from datetime import datetime, timedelta
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15) # Any session will expire after 15 minutes
# Settings to remove the whitespaces added by jinja blocks
app.jinja_env.lstrip_blocks = True 
app.jinja_env.trim_blocks = True

# Choose how you feel
@app.route('/', methods=['GET', 'POST'])
def mood_checkin():
    if not 'mood_dict' in session:  # First check if the session has already a saved dictionary
        emotions_api = MoodDict()
        emotions_dict = emotions_api.make_dict()
        session['mood_dict'] = emotions_dict # in case we do want to save the giphy url - delete if not
    return render_template("mood.html", emotions=session['mood_dict'])


# Accessed after choosing a feeling - allows user to choose between getting a joke or a quote
@app.route('/choice/<id>', methods=['GET', 'POST'])
def choice(id):
    session['emotion'] = id
    session['mood_url'] = session['mood_dict'][id] # in case we do want to save the giphy url - delete if not
    return render_template("choice.html", emotion=id)


# Get the quote of the day
@app.route('/quote', methods=['GET', 'POST'])
def quote_of_the_day():
    quote_api = QuoteAPI()
    result = quote_api.unpack()
    quote = result[0]
    author = result[1]
    if request.method == "POST":
        if 'user' not in session:
            return redirect('/login')
        else:
            response = check_entry(session['user_id'], session['date'])
            if response == True:
                flash("You have already saved an entry for today", "notification")
            elif response == False:
                today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Quote', quote)
                response_two = check_entry(session['user_id'], session['date'])
                if response_two:
                    return redirect('/journal')
            else:
                flash("Something went wrong. Please try again later", "error")
    return render_template("quote.html", quote=quote, author=author)


# Get a joke
@app.route('/joke', methods=['GET', 'POST'])
def joke_generator():
    joke_api = JokeAPI()
    result = joke_api.unpack()
    if request.method == "POST":
        if 'user' not in session:
            return redirect('/login')
        else:
            response = check_entry(session['user_id'], session['date'])
            if response == True:
                flash("You have already saved an entry for today", "notification")
            elif response == False:
                today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Joke', result)
                response_two = check_entry(session['user_id'], session['date'])
                if response_two:
                    return redirect('/journal')
            else:
                flash("Something went wrong. Please try again later", "error")
    return render_template("joke.html", joke=result)


# Save a journal entry
@app.route('/journal', methods=['GET', 'POST'])
def add_journal_entry():
    session.pop('_flashes', None)
    if request.method == 'POST':
        content = request.form.get('textarea')
        if 'user' not in session:
            return redirect('/login')
        elif not content:
            flash('Journal is empty', "notification-error")
        else:
            response = check_entry_journal(session['user_id'], session['date'])
            if response == True:
                flash('You have already submitted a diary entry for this date', "notification")
            elif response == False:
                add_journal(content, session['user_id'], session['date'])
                response_two = check_entry_journal(session['user_id'], session['date'])
                if response_two:
                    return redirect('/overview')
            else:
                flash('Something went wrong. Please try again later.', "error")
    return render_template("journal.html")


# Get calendar view of your entries + stats of moods
@app.route('/overview', methods=['GET'])
def show_overview():
    if 'user' not in session:
        return redirect('/login')
    return render_template("overview.html")


# Shows the saved records for a chosen date
@app.route('/archive/<date>')
def show_archive_by_date(date):
    # Get the records from the database
    saved_records = get_records(session['user_id'], date)
    if saved_records is None:
        flash(f"No records saved on {date}")
        return redirect('/overview')
    record = {}
    record['emotion'] = saved_records[0]
    record['gif_url'] = saved_records[1]
    record['choice'] = saved_records[2]
    record['quote_joke'] = saved_records[3]
    record['diary'] = saved_records[4]
    print(record)
    return render_template("archive.html", date=date, record=record)


# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        content = {}
        for item in ["FirstName", "LastName", "Username", "email", "password", "confirm", "accept_tos"]:
            content[item] = request.form.get(item)
        if content['password'] != content['confirm']:
            flash('Password and Password Confirmation do not match', "error")
        else:
            bytes = content['password'].encode('utf-8')
            content['salt'] = bcrypt.gensalt()
            content['hashed_password'] = bcrypt.hashpw(bytes, content['salt'])
            content['salt'] = content['salt'].decode()
            content['hashed_password'] = content['hashed_password'].decode()
        if check_email(content['email']):
            flash('Email already registered')
        elif check_username(content['Username']):
            flash('Username already in use', "error")
        else:
            add_new_user(content)
            if check_email(content['email']):
                flash("Your account has been created. Please login.", "notification")
                return redirect('/login')
            else:
                flash('We were unable to register you at this time. Please try again later', "error")
    return render_template("register.html", form=form)


# Log in with credentials - salting attempt

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session.clear()
        username = request.form.get('uname')
        password = request.form.get('password')

        if not check_username(username):
            flash("This username does not exist")
        else:
            response = verify_cred(username, password)
            password_correct = verify_password(username, password)
            print(password_correct)
            if not response:
                flash("Username and Password do not match")
            elif response:
                session['user'] = username
                session['user_id'] = get_user_id(username)
                session['date'] = datetime.today().strftime('%Y-%m-%d')
                return redirect('/')
            else:
                flash("Something went wrong! Please try again later")
    return render_template("login.html")


# Log in with credentials - not salted

# @app.route('/login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':
#         session.clear()
#         username = request.form.get('uname')
#         password = request.form.get('password')
#         if not check_username(username):
#             flash("This username does not exist")
#         else:
#             response = verify_cred(username, password)
#             if not response:
#                 flash("Username and Password do not match")
#             elif response:
#                 session['user'] = username
#                 session['user_id'] = get_user_id(username)
#                 session['date'] = datetime.today().strftime('%Y-%m-%d')
#                 return redirect('/')
#             else:
#                 flash("Something went wrong! Please try again later")
#     return render_template("login.html")


# Log out and clear the session
@app.route('/logout')
def user_logout():
    session.clear()
    flash("You have been logged out. See you soon!", "notification")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5500)




