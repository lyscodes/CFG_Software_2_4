from db_utils import get_month_emotions, get_user_id, today_emotion, add_new_user, check_email, check_username, get_password, check_entry_journal, check_entry, add_journal, get_records
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from config import SECRET_KEY
from helper_oop import QuoteAPI, JokeAPI, MoodDict
from registration_form import RegistrationForm
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt 


app = Flask(__name__)

# Setting session secret key and a session length of 15 minutes
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Settings to remove the whitespaces added by jinja blocks
app.jinja_env.lstrip_blocks = True 
app.jinja_env.trim_blocks = True

# Sets up encryption for passwords:
bcrypt = Bcrypt(app)


# Homepage displays gifs from the api for the user to select
@app.route('/', methods=['GET'])
def mood_checkin():
    if 'mood_dict' not in session:  # First check if the session has already a saved dictionary
        try:
            emotions_api = MoodDict()
            emotions_dict = emotions_api.make_dict()
            session['mood_dict'] = emotions_dict # saves the gif url dict to the session
        except Exception as e:
            print('Mood endpoint: ', e)
            session.pop('_flashes', None)
            flash("Something went wrong. Please try again later", "error")
    return render_template("mood.html", emotions=session['mood_dict'])


# After choosing a feeling, user is redirected here where they can choose between getting a joke or a quote
@app.route('/choice/<id>', methods=['GET', 'POST'])
def choice(id):
    try: # saves selected mood and gif url into the session
        session['emotion'] = id
        session['mood_url'] = session['mood_dict'][id]
    except Exception as e:
        print('Choice endpoint: ', e)
        session.pop('_flashes', None)
        flash("Something went wrong! Please submit a new choice", "error")
        return redirect('/')
    return render_template("choice.html", emotion=id)


# Page displaying the quote of the day
@app.route('/quote', methods=['GET', 'POST'])
def quote_of_the_day():
    quote_api = QuoteAPI()
    result = quote_api.unpack()
    quote = result[0]
    author = result[1]
    if request.method == "POST": # triggered when the user tries to save the quote
        # following logic checks if they are able to save a quote (are they logged in -> have they already saved an entry for today -> did the entry save?)
        if 'user' not in session:
            return redirect('/login')
        else:
            try:
                validation_check = check_entry(session['user_id'], session['date'])
                if validation_check == True:
                    session.pop('_flashes', None)
                    flash("You have already saved an entry for today", "notification")
                elif validation_check == False:
                    today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Quote', quote)
                    validation_check_two = check_entry(session['user_id'], session['date'])
                    if validation_check_two:
                        return redirect('/journal')
            except Exception as e:
                print('Quote endpoint: ', e)
                session.pop('_flashes', None)
                flash("Something went wrong. Please try again later", "error")
    return render_template("quote.html", quote=quote, author=author)


# Page displaying joke of the day. Follows the same logic:
@app.route('/joke', methods=['GET', 'POST'])
def joke_generator():
    joke_api = JokeAPI()
    result = joke_api.unpack()
    if request.method == "POST":
        if 'user' not in session:
            return redirect('/login')
        else:
            try:
                response = check_entry(session['user_id'], session['date'])
                if response == True:
                    session.pop('_flashes', None)
                    flash("You have already saved an entry for today", "notification")
                elif response == False:
                    today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Joke', result)
                    response_two = check_entry(session['user_id'], session['date'])
                    if response_two:
                        return redirect('/journal')
            except Exception as e:
                print('Joke endpoint: ', e)
                session.pop('_flashes', None)
                flash("Something went wrong. Please try again later", "error")
    return render_template("joke.html", joke=result)


# Page allowed the user to write and save a journal entry
@app.route('/journal', methods=['GET', 'POST'])
def add_journal_entry():
    if request.method == 'POST':
        content = request.form.get('textarea')
        # Series of validation checks before saving the entry
        # (is the user logged in? -> is there content in the journal? -> is the content too long? -> have they saved their mood choice yet? -> have they saved a diary entry already?)
        if 'user' not in session:
            return redirect('/login')
        elif not content:
            session.pop('_flashes', None)
            flash('Journal is empty', "notification-error")
        elif len(content) > 500:
            session.pop('_flashes', None)
            flash("Oops! Journal entries must be 500 characters or less...", "error")
        else:
            try:
                validation_check = check_entry(session['user_id'], session['date'])
                if validation_check == False:
                    session.pop('_flashes', None)
                    flash("You need to save today's emotion first!", "notification")
                elif validation_check == True:
                    validation_check_two = check_entry_journal(session['user_id'], session['date'])
                    if validation_check_two == True:
                        session.pop('_flashes', None)
                        flash('You have already submitted a diary entry for this date', "notification")
                    elif validation_check_two == False:
                        if add_journal(content, session['user_id'], session['date']) == "Diary entry added":
                            session.pop('_flashes', None)
                            flash("Your entry has been saved.", "notification")
                            return redirect('/overview')
                        else:
                            session.pop('_flashes', None)
                            flash('Something went wrong. Please try again later.', "error")
            except Exception as e:
                print('Journal endpoint: ', e)
                session.pop('_flashes', None)
                flash('Something went wrong. Please try again later.', "error")
    return render_template("journal.html")


# This page gets calendar view of your entries + stats of moods
@app.route('/overview', methods=['GET', 'POST'])
def show_overview():
    if 'user' not in session: # checks if the user is logged in, redirects if not
        return redirect('/login')
    if request.method == "POST": # triggered by the calendar changing month
        session.pop('_flashes', None)
        try:
            date = request.form.get('month')
            sliced_date = date[0:15]
            if sliced_date:
                date_object = datetime.strptime(sliced_date, "%a %b %d %Y")
                # Get full month name:
                month_dt = str(date_object.month)
                month_object = datetime.strptime(month_dt, "%m")
                month_name = month_object.strftime("%B")
                # Get month and year as integers:
                month = int(date_object.month)
                year = int(date_object.year)
                # Get array for user's emotions for that month/year
                myList = get_month_emotions(session['user_id'], month, year)
                return jsonify({'output': myList, 'label': f'Your moods for {month_name} {year}...'})
        except Exception as e:
            print('Overview endpoint: ', e)
    return render_template("overview.html")


# Shows the saved records for a chosen date
@app.route('/archive/<date>')
def show_archive_by_date(date):
    if 'user' not in session: # checks if the user is logged in, redirects if not
        return redirect('/login')
    # Get the records from the database
    saved_records = get_records(session['user_id'], date)
    if saved_records is None:
        flash(f"No records saved on {date}", 'notification')
        return redirect('/overview')
    record = {}
    record['emotion'] = saved_records[0]
    record['gif_url'] = saved_records[1]
    record['choice'] = saved_records[2]
    record['quote_joke'] = saved_records[3]
    record['diary'] = saved_records[4]
    if record['diary'] is None:
        record['diary'] = f"Looks like you didn't save one for {date}"
    return render_template("archive.html", date=date, record=record)


# Page to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST': # Triggered when the form is submitted
        content = {}
        # Collect user input from the form:
        for item in ["FirstName", "LastName", "Username", "email", "password", "confirm", "accept_tos"]:
            content[item] = request.form.get(item)
        # A series of validation checks:
        if content['password'] != content['confirm']:
            session.pop('_flashes', None)
            flash('Password and Password Confirmation do not match', "error")
        if check_email(content['email']):
            session.pop('_flashes', None)
            flash('Email already registered')
        elif check_username(content['Username']):
            session.pop('_flashes', None)
            flash('Username already in use', "error")
        else:
            # If checks passed, it now tries to create a hashed_password
            try:
                hashed_password = bcrypt.generate_password_hash(content['password']).decode('utf-8')
                content['hashed_password'] = hashed_password
                if add_new_user(content) == 'New user added.':
                    session.pop('_flashes', None)
                    flash("Your account has been created. Please login.", "notification")
                    return redirect('/login')
                else:
                    session.pop('_flashes', None)
                    flash('We were unable to register you at this time. Please try again later', "error")
            except Exception as e:
                print('New user endpoint: ', e)
                session.pop('_flashes', None)
                flash('We were unable to register you at this time. Please try again later', "error")
    return render_template("register.html", form=form)


# Page for user to login
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST': # Triggered on form submission
        session.clear()
        username = request.form.get('uname')
        password = request.form.get('password')
        if not check_username(username): # Validation check for username
            session.pop('_flashes', None)
            flash("This username does not exist", "error")
        else:
            try:
            # Verifies password matches hashed password
                stored_password = get_password(username)
                if not bcrypt.check_password_hash(stored_password, password):
                    session.pop('_flashes', None)
                    flash("Username and Password do not match", "error")
                else: # If successful, username, id, and date added to the session:
                    session['user'] = username
                    session['user_id'] = get_user_id(username)
                    session['date'] = datetime.today().strftime('%Y-%m-%d')
                    return redirect('/')
            except Exception as e:
                print('Login endpoint: ', e)
                flash("Something has gone wrong. Please try again later", "error")
    return render_template("login.html")


# Log out and clear the session
@app.route('/logout')
def user_logout():
    session.clear()
    flash("You have been logged out. See you soon!", "notification")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5500)

