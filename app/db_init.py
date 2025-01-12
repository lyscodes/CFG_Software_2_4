from data.entries_data import entries_dd
from data.user_data import localusers_dd, users_dd
from app.models.entries import Entries
from app.models.localuser import LocalUser
from app.models.user import User
from app import db

def initialize_dummy_data():

    if User.query.count() == 0 and Entries.query.count():
        for user in users_dd:
            new_user = User(username=user[0], email=user[1])
            db.session.add(new_user)
            db.session.commit()

        for localuser in localusers_dd:
            new_user = LocalUser(user_id=localuser[0], first_name=localuser[1], family_name=localuser[2],
                             password=localuser[3], accept_tos=localuser[4])
            db.session.add(new_user)
            db.session.commit()

        for entry in entries_dd:
            new_entry = Entries(user_id=entry[0], entry_date=entry[1], emotion=entry[2], giphy_url=entry[3],
                            choice=entry[4], content=entry[5], diary_entry=entry[6])
            db.session.add(new_entry)
            db.session.commit()