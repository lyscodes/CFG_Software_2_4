import mysql.connector
from config import DB_CONFIG



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

    def close_connection(self):
        if self.connection:
            self.connection.close()
            return "DB connection closed."

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
        except Exception:
            raise DbConnectionError
        finally:
            value = self.cur.fetchall()
            print(self.close_connection())
            return value



# VALIDATION QUERIES:

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
    except Exception as e:
        print('Validation check error', e)
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
    except Exception as e:
        print('Validation check error', e)
    finally:
        return validation_check


def check_username(username):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT User_Name FROM Users
                WHERE User_Name = '{input_to_check}');""".format(
            input_to_check=username
        )
        validation_check = db.fetch_data(query)[0][0]
    except Exception as e:
        print('Validation check error', e)
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
    except Exception as e:
        print("Something went wrong when trying to validate the entry", e)

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
    try:
        return db.fetch_data(query)[0]
    except Exception as e:
        print('Get records function:', e)
        return None


# Get journal entry from date
def get_journal_entry(user_id, date):
    query = """
        SELECT Diary_Entry
        FROM Entries
        WHERE User_ID = '{user}' 
        AND Entry_Date = '{date}';
        """.format(user=user_id, date=date)
    try:
        db = DbConnection()
        return db.fetch_data(query)[0][0]
    except Exception as e:
        print(e)
        return None

# Get the user id from db
def get_user_id(username):
    query = """SELECT ID FROM Users
        WHERE User_Name = '{user}' LIMIT 1;""".format(user=username)
    try:
        db = DbConnection()
        return db.fetch_data(query)[0][0]
    except Exception as e:
        print(e)
        return None


# Retrieve hashed_password
def get_password(username):
    try:
        db = DbConnection()
        query = """SELECT Password FROM Users
                    WHERE User_Name = '{Username}'""".format(
                Username=username
            )
        return db.fetch_data(query)[0][0]
    except Exception as e:
        print('Unable to verify password', e)
        return None


def get_month_emotions(user_id, month, year):
    query = """SELECT emotion, COUNT(Emotion)
            FROM Entries
            WHERE  User_ID = {user_id}
            AND MONTH(Entry_Date) = {month}
            AND YEAR(Entry_Date) = {year}
            group by emotion""".format(user_id=user_id, month=month, year=year)
    try:
        db = DbConnection()
        return order_month_data(db.fetch_data(query))
    except Exception as e:
        print(e)
        return None


# Organise the month data in the order needed for the frontend
def order_month_data(data):
    my_data = dict(data)
    myList = ["angry", "calm", "frustrated", "happy", "sad", "worried"]
    for i in range(len(myList)):
        if myList[i] not in my_data:
            myList[i] = 0
        else:
            myList[i] = my_data[myList[i]]
    return myList


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
    except Exception as e:
        print('Unable to save emotion / response', e)


def add_new_user(user):
    try:
        db = DbConnection()
        query = """INSERT INTO Users (First_Name, Family_Name, User_Name, Email, Password)
                VALUES('{FirstName}', '{LastName}', '{Username}', '{email}', "{password}")""".format(
            FirstName=user['FirstName'],
            LastName=user['LastName'],
            Username=user['Username'],
            email=user['email'],
            password=user['hashed_password'])
        print(query)
        db.commit_data(query)
    except Exception as e:
        print('Unable to add new user', e)


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
    except Exception as e:
        print("Some exception was raised when trying to add entry", e)

