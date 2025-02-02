from config import DB_CONFIG
from mysql.connector import connection


# create connector without db name
class BaseConnection():
    def __init__(self):
        self.cnx = connection.MySQLConnection(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            auth_plugin='mysql_native_password'
        )
        self.cur = self.cnx.cursor()

    def close_connection(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            return "DB connection closed."
        return "No connection to close."


def create_db_from_file(sql_file):
    with open(sql_file, encoding="cp437") as file:
        sql_script = file.read()
    queries = sql_script.split(';\n')

    db = BaseConnection()

    for query in queries:

        try:
            db.cur.execute(query)
            db.cnx.commit()
            print("Query run: ", query)  # To verify in the terminal that all queries were executed
        except Exception as e:
            print(f"Failed to execute query: {query}", e)
    
    db.close_connection()
    return True


if __name__ == "__main__":
    if create_db_from_file("../DB_Setup/db_create.sql"):
        print(create_db_from_file("../DB_Setup/db_populate.sql"))
