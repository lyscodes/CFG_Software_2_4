from app import db
from app.models.entries import Entries
from app.models.user import User
from app.models.localuser import LocalUser
from app.models.authuser import AuthUser
from sqlalchemy.sql import exists



def today_emotion(user_id, emotion, giphy_url, date, choice, response):
    new_entry = Entries(user_id, emotion, giphy_url, date, choice, response)
    db.session.add(new_entry)
    db.session.commit()


def add_journal(entry, user, date):
    user_entry = Entries.query.filter_by(entry_date=date, user_id=user).all()
    user_entry.diary_entry = entry
    db.session.commit()


def get_user_id_by_username(username):
    return User.query.filter_by(username=username).first().id


def get_user_id_by_email(email):
    return User.query.filter_by(email=email).first().id


def get_password(user_id):
    return LocalUser.query.filter_by(user_id=user_id).first().password


def add_new_global_user(user):
    new_user = User(user['username'], user['email'])
    db.session.add(new_user)
    db.session.commit()


def add_new_local_user(user):
    new_user = LocalUser(user['user_id'], user['FirstName'], user['LastName'], user['password'])
    db.session.add(new_user)
    db.session.commit()


def add_new_auth_user(user):
    new_user = AuthUser(user['user_id'], user['auth_id'], user['name'])
    db.session.add(new_user)
    db.session.commit()


def check_email(email):
    return db.session.query(exists().where(User.query.filter_by(email=email))).scalar()


def check_username(username):
    return db.session.query(exists().where(User.query.filter_by(username=username))).scalar()


def check_entry(user_id, date):
    return db.session.query(exists().where(Entries.query.filter_by(user_id=user_id, diary_entry=date))).scalar()


def get_records(user_id, date):
    return Entries.query.filter_by(user_id=user_id, entry_date=date).First()


def check_journal_entry(user_id, date):
    entry = Entries.query.filter_by(user_id=user_id, entry_date=date).First()
    if entry is not None and entry.diary_entry is not None:
        return True
    return False


def order_month_data(data):
    emotion_data = dict(data)
    emotion_list = ["angry", "calm", "frustrated", "happy", "sad", "worried"]
    for i in range(len(emotion_list)):
        if emotion_list[i] not in emotion_data:
            emotion_list[i] = 0
        else:
            emotion_list[i] = emotion_data[emotion_list[i]]
    return emotion_list


def get_mont_emotions(user_id, month, year):
    all_user_entries = Entries.query.filter_by(user_id=user_id).all()
    # filter by month and year here
    return order_month_data(all_user_entries)





