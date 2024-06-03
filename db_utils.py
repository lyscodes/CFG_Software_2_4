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


# VALIDATION QUERIES:

# check if already in
def check_entry(user_id, date):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        value_query = """SELECT EXISTS (SELECT Entry_Date FROM Entries
                WHERE Entry_Date = '{date}' AND User_ID = '{user_id}');""".format(
            date=date,
            user_id=user_id
        )
        print(value_query)
        cur.execute(value_query)
        validation_check = cur.fetchall()[0][0]
    except Exception:
        print('Validation check error')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
        return validation_check

def check_email(email):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        value_query = """SELECT EXISTS (SELECT Email FROM users
                WHERE Email = '{input_to_check}');""".format(
            input_to_check=email
        )
        cur.execute(value_query)
        validation_check = cur.fetchall()[0][0]
    except Exception:
        print('Validation check error')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
    return validation_check


def check_username(username):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        value_query = """SELECT EXISTS (SELECT User_Name FROM users
                WHERE User_Name = '{input_to_check}');""".format(
            input_to_check=username
        )
        cur.execute(value_query)
        validation_check = cur.fetchall()[0][0]
    except Exception:
        print('Validation check error')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
    return validation_check


def verify_cred(username, password):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        ver_query = """SELECT EXISTS (SELECT User_Name FROM Users
                WHERE User_Name = '{Username}' AND Password = '{password}');""".format(
            Username=username,
            password=password
        )
        print(ver_query)
        cur.execute(ver_query)
        validation_check = cur.fetchall()[0][0]
    except Exception:
        print('Unable to verify password')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
        return validation_check

def check_entry_journal(user, date):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")

        cur = db_connection.cursor()

        query = """SELECT EXISTS(
            SELECT Diary_Entry
            FROM Entries
            WHERE User_ID = '{user_id}' 
            AND Entry_Date = '{date}'
            AND Diary_Entry IS NOT NULL);
            """.format(user_id=user, date=date)
        cur.execute(query)
        validation_check = cur.fetchall()[0][0]
        cur.close()

    except Exception:
        print("Something went wrong when trying to get the entry")

    finally:
        if db_connection:
            db_connection.close()
        return validation_check


# RETRIEVE QUERIES:

# Get all the records for a date
def get_records(user_id, date):
    record = None
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")
        cur = db_connection.cursor()
        query = """
            SELECT 
            Emotion,
            Giph_URL,
            Choice_J_or_Q,
            Response_J_or_Q,
            Diary_Entry
            FROM Entries
            WHERE User_ID = '{user}' 
            AND Entry_Date = '{date}';
            """.format(user=user_id, date=date)
        print(query)
        cur.execute(query)
        record = cur.fetchone()
        cur.close()
    except Exception:
        print("Something went wrong when trying to get the entry")
    finally:
        if db_connection:
            db_connection.close()
        return record


# Get journal entry from date
def get_journal_entry(user_id, date):
    result_entry = "Oops! Looks like there is no entry on this date"
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")
        cur = db_connection.cursor()
        query = """
            SELECT Diary_Entry
            FROM Entries
            WHERE User_ID = '{user}' 
            AND Entry_Date = '{date}';
            """.format(user=user_id, date=date)
        print(query)
        cur.execute(query)
        result_entry = cur.fetchall()
        cur.close()
    except Exception:
        print("Something went wrong when trying to get the entry")
    finally:
        if db_connection:
            db_connection.close()
        return result_entry


# Get the user id from db
def get_user_id(username):
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        value_query = """SELECT ID FROM Users
            WHERE User_Name = '{user}' LIMIT 1;""".format(user=username)
        cur.execute(value_query)
        user_ID = cur.fetchall()[0][0]
    except Exception:
        print('Unable to save emotion / response')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
        return user_ID


def get_month_emotions(user_id, month, year):
    dict = {'happy': 3,
            'calm': 4,
            'sad': 5,
            'worried': 10,
            'frustrated': 12,
            'angry': 1}
    return dict


# COMMIT QUERIES:

# Record mood choice in db
def today_emotion(user_id, emotion, giphy_url, date, choice, response):
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        add_query = """INSERT INTO Entries (User_ID, Entry_Date, Emotion, Giph_URL, Choice_J_or_Q, Response_J_or_Q )
                VALUES('{UserID}', '{EntryDate}', '{Emotion}', '{URL}', '{Choice}', '{Response}');""".format(
            UserID=user_id,
            EntryDate=date,
            Emotion=emotion,
            URL=giphy_url,
            Choice=choice,
            Response=response
        )
        print(add_query)
        cur.execute(add_query)
        db_connection.commit()
    except Exception:
        print('Unable to save emotion / response')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')



def add_new_user(user):
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        add_query = """INSERT INTO Users (First_Name, Family_Name, User_Name, Email, Password)
                VALUES('{FirstName}', '{LastName}', '{Username}', '{email}', '{password}');""".format(
            FirstName=user['FirstName'],
            LastName=user['LastName'],
            Username=user['Username'],
            email=user['email'],
            password=user['password']
        )
        cur.execute(add_query)
        db_connection.commit()
    except Exception:
        print('Unable to add new user')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')


# Record new journal entry in db
def add_journal(entry, user, date):
    try:
        db_connection = _connect_to_db(db_name)
        if not db_connection:
            raise DbConnectionError("Failed to connect to DB")

        cur = db_connection.cursor()
        query = """
                UPDATE Entries 
                SET Diary_Entry = '{entry}'
                WHERE User_ID = '{user_id}' AND Entry_Date = '{date}';
                """.format(user_id=user, date=date, entry=entry)
        print(query)
        cur.execute(query)
        db_connection.commit()
        cur.close()

    except Exception:
        print("Some exception was raised when trying to add entry")

    finally:
        if db_connection:
            db_connection.close()


