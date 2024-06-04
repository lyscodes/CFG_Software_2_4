import mysql.connector
from config import DB_CONFIG
from functools import wraps


class DbConnectionError(Exception):
    pass


class DbConnection:

    DB_NAME = 'Mood_Tracker'

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            auth_plugin='mysql_native_password',
            database=DbConnection.DB_NAME
            )
        self.cur = self.connection.cursor()        


    def commit_data(self, query):
        try:
            self.cur.execute(query)
            self.connection.commit()
        except Exception:
            raise DbConnectionError
        finally:
            print(self.close_connection())


    def fetch_data(self, query):
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception:
            raise DbConnectionError
        finally:
            print(self.close_connection())


    def close_connection(self):
        if self.connection:
            self.connection.close()
            return "DB connection closed."


# VALIDATION QUERIES:

# check if already in
def check_entry(user_id, date):
    validation_check = False
    try:
        db= DbConnection()
        query = """SELECT EXISTS (SELECT Entry_Date FROM Entries
                WHERE Entry_Date = '{date}' AND User_ID = '{user_id}');""".format(
            date=date,
            user_id=user_id
        )
        validation_check = db.fetch_data(query)[0][0]
    except Exception:
        print('Validation check error')
    finally:
        return validation_check


def check_email(email):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT Email FROM users
                WHERE Email = '{input_to_check}');""".format(
            input_to_check=email
        )
        
        validation_check = db.fetch_data(query)[0][0]
    except Exception:
        print('Validation check error')
    finally:
        return validation_check


def check_username(username):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT User_Name FROM users
                WHERE User_Name = '{input_to_check}');""".format(
            input_to_check=username
        )
        validation_check = db.fetch_data(query)[0][0]
    except Exception:
        print('Validation check error')
    finally:
        return validation_check


def verify_cred(username, password):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT User_Name FROM Users
                    WHERE User_Name = '{Username}' AND Password = '{password}');""".format(
                Username=username,
                password=password
            )

        validation_check = db.fetch_data(query)[0][0]
    except Exception:
        print('Unable to verify password')
    finally:
        return validation_check



def check_entry_journal(user, date):
    validation_check = False
    try:
        db = DbConnection()

        query = """SELECT EXISTS(
            SELECT Diary_Entry
            FROM Entries
            WHERE User_ID = '{user_id}' 
            AND Entry_Date = '{date}'
            AND Diary_Entry IS NOT NULL);
            """.format(user_id=user, date=date)

        validation_check = db.fetch_data(query)[0][0]

    except Exception:
        print("Something went wrong when trying to get the entry")

    finally:
        return validation_check


# RETRIEVE QUERIES:

# Get all the records for a date
def get_records(user_id, date):
    db = DbConnection()
    
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

    return db.fetch_data(query)[0]


# Get journal entry from date
def get_journal_entry(user_id, date):
    result_entry = "Oops! Looks like there is no entry on this date"
    db = DbConnection()
    query = """
        SELECT Diary_Entry
        FROM Entries
        WHERE User_ID = '{user}' 
        AND Entry_Date = '{date}';
        """.format(user=user_id, date=date)
    return db.fetch_data(query)[0][0]


# Get the user id from db
def get_user_id(username):
    db = DbConnection()

    query = """SELECT ID FROM Users
        WHERE User_Name = '{user}' LIMIT 1;""".format(user=username)

    return db.fetch_data(query)[0][0]


def get_month_emotions(user_id, year, month):
    month = month # need to pull month from the date inputted
    year = year # need to pull year from the date inputted
    dict = {'happy': 40,
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
        db = DbConnection()
        query = """INSERT INTO Entries (User_ID, Entry_Date, Emotion, Giph_URL, Choice_J_or_Q, Response_J_or_Q )
                VALUES('{UserID}', '{EntryDate}', '{Emotion}', '{URL}', '{Choice}', '{Response}');""".format(
            UserID=user_id,
            EntryDate=date,
            Emotion=emotion,
            URL=giphy_url,
            Choice=choice,
            Response=response
        )
        db.commit_data(query)
    except Exception:
        print('Unable to save emotion / response')


def add_new_user(user):
    try:
        db = DbConnection()
        query = """INSERT INTO Users (First_Name, Family_Name, User_Name, Email, Password)
                VALUES('{FirstName}', '{LastName}', '{Username}', '{email}', '{password}');""".format(
            FirstName=user['FirstName'],
            LastName=user['LastName'],
            Username=user['Username'],
            email=user['email'],
            password=user['password']
        )
        db.commit_data(query)
    except Exception:
        print('Unable to add new user')


# Record new journal entry in db
def add_journal(entry, user, date):
    try:
        db = DbConnection()
        query = """
                UPDATE Entries 
                SET Diary_Entry = '{entry}'
                WHERE User_ID = '{user_id}' AND Entry_Date = '{date}';
                """.format(user_id=user, date=date, entry=entry)
        db.commit_data(query)
    except Exception:
        print("Some exception was raised when trying to add entry")


