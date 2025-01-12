from app.db_utils import *
from app.helper import QuoteAPI, JokeAPI, MoodDict
from app.forms.registration_form import RegistrationForm
from flask import render_template, request, flash, redirect, session, url_for
from datetime import datetime
from app.dateutils import get_utc_date, get_month_name
from functools import wraps
from flask import Blueprint, jsonify
from app.oauth_providers import googleOauth
from app import bcrypt

main = Blueprint('main', __name__)


def flash_error(error):
    session.pop('_flashes', None)
    flash(error, "error")


def flash_notification(notification):
    session.pop('_flashes', None)
    flash(notification, 'notification')



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.user_login'))
    return wrap


@main.errorhandler(Exception)
def error_handler(error):
    print(f"Error occurred at route: {request.path} (method: {request.method}) - Error: {error}")
    flash_error("Something went wrong. Please try again later")
    if request.referrer:
        return redirect(request.referrer)
    return redirect('/')


@main.route('/', methods=['GET'])
def mood_checkin():
    if 'mood_dict' not in session:
        emotions_api = MoodDict()
        emotions_dict = emotions_api.make_dict()
        session['mood_dict'] = emotions_dict
    return render_template("mood.html", emotions=session['mood_dict'])


@main.route('/choice/<emotion_id>', methods=['GET', 'POST'])
def choice(emotion_id):
    session['emotion'] = emotion_id
    session['mood_url'] = session['mood_dict'][emotion_id]
    return render_template("choice.html", emotion=emotion_id)


@main.route('/save_choice', methods=['GET'])
@login_required
def save_choice():
    choice = session['choice']
    entry_saved_already = check_entry(session['user_id'], session['date'])
    if entry_saved_already:
        flash_notification("You have already saved an entry for today")
    else:
        today_emotion(session['user_id'], session['emotion'], session['mood_url'], session['date'], session['choice'], session[choice])
        if check_entry(session['user_id'], session['date']):
            flash_notification("Your entry has been saved.")
            return redirect('/journal')
        else:
            flash_error("Something went wrong. Please try again later")
            return redirect('/')
    return redirect(f'/{choice}')


@main.route('/quote', methods=['GET', 'POST'])
def quote_of_the_day():
    if 'quote' not in session:
        quote_api = QuoteAPI()
        result = quote_api.unpack()
        session['quote'] = result[0]
        session['author'] = result[1]
    if request.method == "POST":
        session['choice'] = "quote"
        return redirect('/save_choice')
    return render_template("quote.html", quote=session['quote'], author=session['author'])


@main.route('/joke', methods=['GET', 'POST'])
def joke_generator():
    if 'joke' not in session:
        joke_api = JokeAPI()
        result = joke_api.unpack()
        session['joke'] = result
    if request.method == "POST":
        session['choice'] = "joke"
        return redirect('/save_choice')
    return render_template("joke.html", joke=session['joke'])


@main.route('/journal', methods=['GET', 'POST'])
@login_required
def add_journal_entry():
    if request.method == 'POST':
        content = request.form.get('textarea')
        if not content:
            flash_error('Journal is empty')
        elif len(content) > 350:
            flash_error("Oops! Journal entries must be 350 characters or less...")
        else:
            if not check_entry(session['user_id'], session['date']):
                flash_notification("You need to save today's emotion first!")
            elif check_journal_entry(session['user_id'], session['date']):
                flash_notification('You have already submitted a diary entry for this date')
            else:
                add_journal(content, session['user_id'], session['date'])
                did_entry_save = check_journal_entry(session['user_id'], session['date'])
                if did_entry_save:
                    flash_notification("Your entry has been saved.")
                    return redirect('/overview')
                else:
                    flash_error('Something went wrong. Please try again later.')
    return render_template("journal.html")


@main.route('/overview', methods=['GET', 'POST'])
@login_required
def show_overview():
    if request.method == "POST":
        session.pop('_flashes', None)
        user_month = request.form.get('month')[0:15]
        if user_month:
            date_object = datetime.strptime(user_month, "%a %b %d %Y")
            emotion_list = get_month_emotions(session['user_id'], int(date_object.month), int(date_object.year))
            return jsonify({'output': emotion_list, 'label': f'Your moods for {get_month_name(date_object)} {int(date_object.year)}...'})
    return render_template("overview.html")


@main.route('/archive/<date>')
@login_required
def show_archive_by_date(date):
    saved_records = get_records(session['user_id'], date)
    if saved_records is None:
        flash_notification(f"No records saved on {date}")
        return redirect('/overview')
    record = {'emotion': saved_records[0], 'gif_url': saved_records[1], 'choice': saved_records[2], 'quote_joke': saved_records[3],
              'diary': f"You didn't feel like journaling on {date} and that's okay!" if saved_records[4] is None else saved_records[4]}
    return render_template("archive.html", date=date, record=record)


@main.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        user_form = {}
        for item in ["FirstName", "LastName", "Username", "email", "password", "confirm", "accept_tos"]:
            user_form[item] = request.form.get(item)
        if user_form['password'] != user_form['confirm']:
            flash_error('Password and Password Confirmation do not match')
        elif check_email(user_form['email']):
            flash_error('Email already registered')
        elif check_username(user_form['Username']):
            flash_error('Username already in use')
        else:
            user_form['password'] = bcrypt.generate_password_hash(user_form['password']).decode('utf-8')
            if add_new_user(user_form) == 'New user added.':
                flash_notification("Your account has been created. Please login.")
                return redirect('/login')
            else:
                flash_error('We were unable to register you at this time. Please try again later')
    return render_template("register.html", form=form)


@main.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        session.clear()
        username = request.form.get('uname')
        password = request.form.get('password')
        if not check_username(username):
            flash_error("This username does not exist")
        else:
            stored_password = get_password(username)
            if not bcrypt.check_password_hash(stored_password, password):
                flash_error("Username and Password do not match")
            else:
                session['user'] = username
                session['user_id'] = get_user_id(username)
                session['date'] = get_utc_date()
                return redirect('/')
    return render_template("login.html")


@main.route('/login/google')
def login_google():
    return googleOauth.authorize_redirect(redirect_uri=url_for("main.authorize_google", _external=True))


@main.route('/authorize/google')
def authorize_google():
    token = googleOauth.authorize_access_token()
    userinfo_endpoint = googleOauth.server_metadata['userinfo_endpoint']
    user_info = googleOauth.get(userinfo_endpoint).json()
    session['oauth_token'] = token
    session['user_id'] = user_info['sub']
    session['date'] = get_utc_date()
    session['user'] = user_info['email']
    return redirect("/")


@main.route('/logout')
@login_required
def user_logout():
    session.clear()
    flash_notification("You have been logged out. See you soon!")
    return redirect('/')


