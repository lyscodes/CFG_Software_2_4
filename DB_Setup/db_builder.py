from db_utils import DbConnection


def create_db_from_file(sql_file):
    with open(sql_file, encoding="cp437") as file:
        sql_script = file.read()
    sql_queries = sql_script.split(';\n')
    db = DbConnection()
    for query in sql_queries:
        try:
            db.cur.execute(query)
        except Exception as e:
            print(f"Failed to execute query: {query}", e)
    db.cnx.commit()
    db.close_connection()
    return f"{sql_file} in DB"


if __name__ == "__main__":
    if (create_db_from_file("db_create.sql") == "db_create.sql in DB"):
        print(create_db_from_file("db_populate.sql"))
