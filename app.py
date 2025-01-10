from db_utils import get_month_emotions, get_user_id, today_emotion, add_new_user, check_email, check_username, get_password, check_entry_journal, check_entry, add_journal, get_records
from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from config import SECRET_KEY, AUTH0_CLIENT_SECRET, AUTH0_CLIENT_ID
from helper_oop import QuoteAPI, JokeAPI, MoodDict
from registration_form import RegistrationForm
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import json
# from os import environ as env -> env emails

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

bcrypt = Bcrypt(app)

oauth = OAuth(app)
googleOauth = oauth.register(
    name="auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://accounts.google.com/.well-known/openid-configuration'
)


@app.route('/', methods=['GET'])
def mood_checkin():
    if 'mood_dict' not in session:
        try:
            emotions_api = MoodDict()
            emotions_dict = emotions_api.make_dict()
            session['mood_dict'] = emotions_dict
        except Exception as e:
            print('Mood endpoint: ', e)
            session.pop('_flashes', None)
            flash("Something went wrong. Please try again later", "error")
    return render_template("mood.html", emotions=session['mood_dict'])


@app.route('/choice/<id>', methods=['GET', 'POST'])
def choice(id):
    try:
        session['emotion'] = id
        session['mood_url'] = session['mood_dict'][id]
    except Exception as e:
        print('Choice endpoint: ', e)
        session.pop('_flashes', None)
        flash("Something went wrong! Please submit a new choice", "error")
        return redirect('/')
    return render_template("choice.html", emotion=id)


@app.route('/quote', methods=['GET', 'POST'])
def quote_of_the_day():
    quote_api = QuoteAPI()
    result = quote_api.unpack()
    quote = result[0]
    author = result[1]
    if request.method == "POST":
        if 'user' not in session:
            return redirect('/login')
        try:
            validation_check = check_entry(session['user_id'], session['date'])
            if validation_check == True:
                session.pop('_flashes', None)
                flash("You have already saved an entry for today", "notification")
            elif validation_check == False:
                today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Quote', quote)
                validation_check_two = check_entry(session['user_id'], session['date'])
                if validation_check_two:
                    session.pop('_flashes', None)
                    flash("Your entry has been saved.", "notification")
                    return redirect('/journal')
                else:
                    session.pop('_flashes', None)
                    flash("Something went wrong. Please try again later", "error")
        except Exception as e:
            print('Quote endpoint: ', e)
            session.pop('_flashes', None)
            flash("Something went wrong. Please try again later", "error")
    return render_template("quote.html", quote=quote, author=author)


@app.route('/joke', methods=['GET', 'POST'])
def joke_generator():
    if 'joke' not in session:
        joke_api = JokeAPI()
        result = joke_api.unpack()
        session['joke'] = result
    if request.method == "POST":
        if 'user' not in session:
            return redirect('/login')
        try:
            v_check = check_entry(session['user_id'], session['date'])
            if v_check == True:
                session.pop('_flashes', None)
                flash("You have already saved an entry for today", "notification")
            elif v_check == False:
                today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], 'Joke', session['joke'])
                vc_two = check_entry(session['user_id'], session['date'])
                if vc_two:
                    session.pop('_flashes', None)
                    flash("Your entry has been saved.", "notification")
                    return redirect('/journal')
                else:
                    session.pop('_flashes', None)
                    flash("Something went wrong. Please try again later", "error")
        except Exception as e:
            print('Joke endpoint: ', e)
            session.pop('_flashes', None)
            flash("Something went wrong. Please try again later", "error")
    return render_template("joke.html", joke=session['joke'])


@app.route('/journal', methods=['GET', 'POST'])
def add_journal_entry():
    if request.method == 'POST':
        content = request.form.get('textarea')
        if 'user' not in session:
            return redirect('/login')
        elif not content:
            session.pop('_flashes', None)
            flash('Journal is empty', "notification-error")
        elif len(content) > 350:
            session.pop('_flashes', None)
            flash("Oops! Journal entries must be 350 characters or less...", "error")
        else:
            try:
                validation_check = check_entry(session['user_id'], session['date'])
                if not validation_check:
                    session.pop('_flashes', None)
                    flash("You need to save today's emotion first!", "notification")
                elif validation_check:
                    validation_check_two = check_entry_journal(session['user_id'], session['date'])
                    if validation_check_two:
                        session.pop('_flashes', None)
                        flash('You have already submitted a diary entry for this date', "notification")
                    elif not validation_check_two:
                        add_journal(content, session['user_id'], session['date'])
                        validation_three = check_entry_journal(session['user_id'], session['date'])
                        if validation_three:
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


@app.route('/overview', methods=['GET', 'POST'])
def show_overview():
    if 'user' not in session:
        return redirect('/login')
    if request.method == "POST":
        session.pop('_flashes', None)
        try:
            date = request.form.get('month')
            sliced_date = date[0:15]
            if sliced_date:
                date_object = datetime.strptime(sliced_date, "%a %b %d %Y")
                month_dt = str(date_object.month)
                month_object = datetime.strptime(month_dt, "%m")
                month_name = month_object.strftime("%B")
                month = int(date_object.month)
                year = int(date_object.year)
                myList = get_month_emotions(session['user_id'], month, year)
                return jsonify({'output': myList, 'label': f'Your moods for {month_name} {year}...'})
        except Exception as e:
            print('Overview endpoint: ', e)
    return render_template("overview.html")


@app.route('/archive/<date>')
def show_archive_by_date(date):
    if 'user' not in session:
        return redirect('/login')
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
        record['diary'] = f"You didn't feel like journaling on {date} and that's okay!"
    return render_template("archive.html", date=date, record=record)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        content = {}
        for item in ["FirstName", "LastName", "Username", "email", "password", "confirm", "accept_tos"]:
            content[item] = request.form.get(item)
        if content['password'] != content['confirm']:
            session.pop('_flashes', None)
            flash('Password and Password Confirmation do not match', "error")
        elif check_email(content['email']):
            session.pop('_flashes', None)
            flash('Email already registered')
        elif check_username(content['Username']):
            session.pop('_flashes', None)
            flash('Username already in use', "error")
        else:
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


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session.clear()
        username = request.form.get('uname')
        password = request.form.get('password')
        if not check_username(username):
            session.pop('_flashes', None)
            flash("This username does not exist", "error")
        else:
            try:
                stored_password = get_password(username)
                if not bcrypt.check_password_hash(stored_password, password):
                    session.pop('_flashes', None)
                    flash("Username and Password do not match", "error")
                else:
                    session['user'] = username
                    session['user_id'] = get_user_id(username)
                    session['date'] = datetime.today().strftime('%Y-%m-%d')
                    return redirect('/')
            except Exception as e:
                print('Login endpoint: ', e)
                flash("Something has gone wrong. Please try again later", "error")
    return render_template("login.html")


@app.route('/login/google')
def login_google():
    try:
        return googleOauth.authorize_redirect(
        redirect_uri=url_for("authorize_google", _external=True)
         )
    except Exception as e:
        app.logger.error(f"Error during google login {str(e)}")
        return "Error occured during login", 500

@app.route('/authorize/google')
def authorize_google():
    token = googleOauth.authorize_access_token()
    userinfo_endpoint = googleOauth.server_metadata['userinfo_endpoint']
    resp = googleOauth.get(userinfo_endpoint)
    user_info = resp.json()
    username = user_info['email']
    print(user_info)
    session['user_id'] = int(user_info['sub'])
    session['date'] = datetime.today().strftime('%Y-%m-%d')
    session['user'] = username
    session['oauth_token'] = token
    return redirect("/")


@app.route('/logout')
def user_logout():
    oauth = session.get('oauth_token')
    session.clear()
    flash("You have been logged out. See you soon!", "notification")
    # if oauth:
    #     return redirect(
    #         "https://accounts.google.com/."
    #         + "/v2/logout?"
    #         + urlencode(
    #             {
    #                 "returnTo": url_for("home", _external=True),
    #                 "client_id": AUTH0_CLIENT_ID,
    #             },
    #             quote_via=quote_plus,
    #         )
    #     )
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5500)

