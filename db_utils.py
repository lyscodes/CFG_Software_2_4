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
def today_emotion(user, emotion, date, response):
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        add_query = """INSERT INTO Entries (User_Name, Entry_Date, Emotion, Response, Diary_Entry)
                VALUES('{Username}', '{EntryDate}', '{Emotion}', '{Response}');""".format(
            Username=user,
            EntryDate=date,
            Emotion=emotion,
            Response=response
        )
        cur.execute(add_query)
        db_connection.commit()
    except Exception:
        print('Unable to save emotion / response')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')

# check if already in
def check_entry(user, date):
    validation_check = False
    try:
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        value_query = """SELECT EXISTS (SELECT Entry_Date FROM Entries
                WHERE Entry_Date = '{date}' AND User_Name = '{user}');""".format(
            date=date,
            user=user
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
        return check_email(user['email'])

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
        cur.execute(ver_query)
        validation_check = cur.fetchall()[0][0]
    except Exception:
        print('Unable to verify password')
    finally:
        if db_connection:
            db_connection.close()
            print('Database connection is closed')
        return validation_check


# Get journal entry from date
def get_journal_entry(user, date):
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
            """.format(user=user, date=date)

        cur.execute(query)
        result = cur.fetchall()
        cur.close()

    except Exception:
        print("Something went wrong when trying to get the entry")

    finally:
        if db_connection:
            db_connection.close()
        return result

# Record new journal entry in db
def add_journal_entry(entry, user, date):
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
                """.format(user=user, date=date, entry=entry)

        cur.execute(query)
        db_connection.commit()
        cur.close()

    except Exception:
        print("Some exception was raised when trying to add entry")

    finally:
        if db_connection:
            db_connection.close()



