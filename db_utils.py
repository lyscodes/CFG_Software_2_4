import mysql.connector
from config import (user, password, host)

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

def today_emotion(emotion, date):
    pass

def journal_entry(entry, date):
    # It should check if the user has already submitted a journal entry for that date
    pass

