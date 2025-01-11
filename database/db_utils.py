from database.config import DB_CONFIG
from mysql.connector import connection
from database.db_builder import BaseConnection


class DbConnection(BaseConnection):

    DB_NAME = 'Mood_Tracker'

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

    def commit_data(self, query, parameters):
        return_message = None
        try:
            self.cur.execute(query, parameters)
            self.cnx.commit()
        except Exception as e:
            return_message = f"Error with db: {e}"
        finally:
            self.close_connection()
            return return_message

    def fetch_data(self, query, parameters):
        try:
            self.cur.execute(query, parameters)
        except Exception as e:
            print("Data not fetched", e)
        finally:
            value = self.cur.fetchall()
            self.close_connection()
            return value


def check_email(email):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT Email FROM users
                WHERE Email = %s);"""
        parameters = (email,)
        validation_check = db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print('Email validation check: ', e)
    finally:
        return validation_check


def check_username(username):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT User_Name FROM Users
                WHERE User_Name = %s);"""
        parameters = (username,)
        validation_check = db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print('Username validation check: ', e)
    finally:
        return validation_check


def check_entry(user_id, date):
    validation_check = False
    try:
        db = DbConnection()
        query = """SELECT EXISTS (SELECT Entry_Date FROM Entries
                WHERE Entry_Date = %s AND User_ID = %s);"""
        parameters = (date, user_id)
        validation_check = db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print('Entry validation check: ', e)
    finally:
        return validation_check


def check_entry_journal(user, date):
    validation_check = False
    try:
        db = DbConnection()

        query = """SELECT EXISTS(
            SELECT Diary_Entry
            FROM Entries
            WHERE User_ID = %s
            AND Entry_Date = %s
            AND Diary_Entry IS NOT NULL);
            """
        parameters = (user, date)
        validation_check = db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print("Journal validation check: ", e)
    finally:
        return validation_check


def get_user_id(username):
    query = """SELECT ID FROM Users
        WHERE User_Name = %s LIMIT 1;"""
    parameters = (username,)
    try:
        db = DbConnection()
        return db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print("Retrieve User ID: ", e)
        return None


def get_password(username):
    try:
        db = DbConnection()
        query = """SELECT Password FROM Users
                    WHERE User_Name = %s"""
        parameters = (username,)
        return db.fetch_data(query, parameters)[0][0]
    except Exception as e:
        print("Get user password: ", e)
        return None


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
        WHERE User_ID = %s
        AND Entry_Date = %s;
        """
    parameters = (user_id, date)
    try:
        return db.fetch_data(query, parameters)[0]
    except Exception as e:
        print("Get user records: ", e)
        return None


def get_month_emotions(user_id, month, year):
    query = """SELECT emotion, COUNT(Emotion)
            FROM Entries
            WHERE  User_ID = %s
            AND MONTH(Entry_Date) = %s
            AND YEAR(Entry_Date) = %s
            group by emotion"""
    parameters = (user_id, month, year)
    try:
        db = DbConnection()
        return order_month_data(db.fetch_data(query, parameters))
    except Exception as e:
        print("Get month emotion stats", e)


def order_month_data(data):
    my_data = dict(data)
    my_list = ["angry", "calm", "frustrated", "happy", "sad", "worried"]
    for i in range(len(my_list)):
        if my_list[i] not in my_data:
            my_list[i] = 0
        else:
            my_list[i] = my_data[my_list[i]]
    return my_list


def add_new_user(user):
    try:
        db = DbConnection()
        query = """INSERT INTO Users (First_Name, Family_Name, User_Name, Email, Password)
                VALUES(%s, %s, %s, %s, %s)"""
        parameters = (user['FirstName'], user['LastName'], user['Username'], user['email'], user['password'])
        db.commit_data(query, parameters)
        return "New user added."
    except Exception as e:
        return f'Unable to add new user. Error: {e}'


def today_emotion(user_id, emotion, giphy_url, date, choice, response):
    try:
        db = DbConnection()
        query = """INSERT INTO Entries (User_ID, Entry_Date, Emotion, Giph_URL, Choice_J_or_Q, Response_J_or_Q )
                VALUES(%s, %s, %s, %s, %s, %s);"""
        parameters = (user_id, date, emotion, giphy_url, choice, response)
        db.commit_data(query, parameters)
    except Exception as e:
        print('Unable to save record: ', e)


def add_journal(entry, user, date):
    try:
        db = DbConnection()
        query = """
                UPDATE Entries 
                SET Diary_Entry = %s
                WHERE User_ID = %s AND Entry_Date = %s;
                """
        parameters = (entry, user, date)
        db.commit_data(query, parameters)
        return "Diary entry added"
    except Exception as e:
        return f"Some exception was raised when trying to add entry. Error: {e}"



