from config import DB_CONFIG
from mysql.connector import connection
from DB_Setup import db_builder


# Connector inherits from base class in db_builder
class DbConnection(db_builder.BaseConnection):

    DB_NAME = 'Mood_Tracker'

    # Add database name to the connection
    def __init__(self):
        super().__init__()
        self.cnx = connection.MySQLConnection(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            auth_plugin='mysql_native_password',
            database=DbConnection.DB_NAME
            )
        self.cur = self.cnx.cursor()

    def commit_data(self, query):
        try:
            self.cur.execute(query)
            self.cnx.commit()
        except Exception as e:
            return f"Error with db: {e}"
        finally:
            self.close_connection()

    def fetch_data(self, query):
        try:
            self.cur.execute(query)
        except Exception as e:
            print("Data not fetched", e)
        finally:
            value = self.cur.fetchall()
            self.close_connection()
            return value



#### VALIDATION QUERIES ####

# Verify that a given email is saved in the Users table
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
        print('Email validation check: ', e)
    finally:
        return validation_check

# Verify that a given username is saved in the Users table
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
        print('Username validation check: ', e)
    finally:
        return validation_check

# Verify if the user has a saved an entry for the given date in the Entries table
def check_entry(user_id, date):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT Entry_Date FROM Entries
                WHERE Entry_Date = '{date}' AND User_ID = '{user_id}');""".format(
            date=date,
            user_id=user_id
        )
        validation_check = db.fetch_data(query)[0][0]
    except Exception as e:
        print('Entry validation check: ', e)
    finally:
        return validation_check

# Verify if the user has a saved diary entry for the given date in the Entries table
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
        print("Journal validation check: ", e)

    finally:
        return validation_check


#### RETRIEVE QUERIES ####

# Get the user id from Users table
def get_user_id(username):
    query = """SELECT ID FROM Users
        WHERE User_Name = '{user}' LIMIT 1;""".format(user=username)
    try:
        db = DbConnection()
        return db.fetch_data(query)[0][0]
    except Exception as e:
        print("Retrieve User ID: ", e)
        return None


# Retrieve hashed_password of a user from Users table
def get_password(username):
    try:
        db = DbConnection()
        query = """SELECT Password FROM Users
                    WHERE User_Name = '{Username}'""".format(
                Username=username
            )
        return db.fetch_data(query)[0][0]
    except Exception as e:
        print("Get user password: ", e)
        return None


# Get all the records for a date in Entries table
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
        print("Get user records: ", e)
        return None

# Retrieve the count of each emotion recorded in a given month in Entries table
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
        print("Get month emotion stats", e)


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


####  COMMIT QUERIES ####

# Record new user in Users table
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
        db.commit_data(query)
        return "New user added."
    except Exception as e:
        return f'Unable to add new user. Error: {e}'


# Record mood choice in Entries table
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
        print(query)
        db.commit_data(query)
    except Exception as e:
        print('Unable to save record: ', e)


# Record new journal entry in Entries table
def add_journal(entry, user, date):
    try:
        db = DbConnection()
        query = """
                UPDATE Entries 
                SET Diary_Entry = '{entry}'
                WHERE User_ID = '{user_id}' AND Entry_Date = '{date}';
                """.format(user_id=user, date=date, entry=entry)
        db.commit_data(query)
        return "Diary entry added"
    except Exception as e:
        return f"Some exception was raised when trying to add entry. Error: {e}"

