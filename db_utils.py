import mysql.connector
from config import (user, password, host)
import datetime

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
    return 1


# Record mood choice in db
def today_emotion(emotion):
    pass


# Get journal entry from date
def get_journal_entry(date):
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")

        cur = db_connection.cursor()

        query = """
            SELECT Diary_Entry
            FROM Entries
            WHERE User_id = {user} 
            AND Entry_Date = DATE('{date}') 
            """.format(user=get_user_id(), date=date)

        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result

    except Exception:
        print("Something went wrong when trying to get the entry")

    finally:
        if db_connection:
            db_connection.close()



# Record new journal entry in db
def add_journal_entry(entry, date):
    # It should check if the user has already submitted a journal entry for that date
    result =  get_journal_entry(date)
    if result == []:
        try:
            db_connection = _connect_to_db(db_name)
            if not db_connection:
                raise DbConnectionError("Failed to connect to DB")

            cur = db_connection.cursor()

            query = """
                INSERT INTO Entries
                (User_ID, Entry_Date, Diary_Entry)
                VALUES
                ({user}, DATE('{date}'), '{entry}')
                """.format(user=get_user_id(), date=date, entry=entry)

            cur.execute(query)
            db_connection.commit()
            cur.close()

        except Exception:
            print("Some exception was raised when trying to add entry")
            return False

        else:
            return True

        finally:
            if db_connection:
                db_connection.close()
    else:
        return False
