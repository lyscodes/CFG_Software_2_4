from app import create_app, db
from data.entries_data import entries_dd
from data.user_data import localusers_dd, users_dd
from app.models.entries import Entries
from app.models.localuser import LocalUser
from app.models.user import User
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
import os
from sqlalchemy import create_engine

app = create_app()

if __name__ == "__main__":

    # can this all move to create app? how does it effect tests?
    with app.app_context():

        load_dotenv()
        engine = create_engine(os.getenv('CONNECTION_STRING')) # using SQLite will not require this
        if not database_exists(engine.url):
            create_database(engine.url)
            db.create_all()

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
                new_entry = Entries(user_id=entry[0], entry_date=entry[1], emotion=entry[2], giphy_url=entry[3], choice=entry[4], content=entry[5], diary_entry=entry[6])
                db.session.add(new_entry)
                db.session.commit()

    app.run(ssl_context=('certs/certificate.pem', 'certs/private.pem'), host='0.0.0.0', port=443)
