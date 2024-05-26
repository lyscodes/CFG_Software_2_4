import mysql.connector
from config import (user, password, host)

db_name = 'Mood_Tracker'

class DbConnectionError(Exception):
    pass

def _connect_to_db(db_name):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return connection


# Get the user id from db
def get_user_id():
    pass


# Record mood choice in db
def today_emotion(emotion):
    pass


# Record new journal entry in db
def journal_entry(entry, date):
    # It should check if the user has already submitted a journal entry for that date
    
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")
        
        cur = db_connection.cursor()

        query = """
            INSERT INTO Entries
            (User_ID, Entry_Date, Diary_Entry)
            VALUES
            (`{user}`, `{date}`, `{entry}`)
            """.format(user=get_user_id(), date=date, entry=entry)

        cur.execute(query)
        db_connection.commit()
        cur.close()

    except Exception:
        return False
    
    else:
        return True
    
    finally:
        if db_connection:
            db_connection.close()
