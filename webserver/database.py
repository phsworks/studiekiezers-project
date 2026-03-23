import MySQLdb
db = None

def db_connect(host, user, password, database):
    try:
        db = MySQLdb.connect(host=host, user=user, password=password, database=database)
        return db
    except MySQLdb.Error as e:
        print(f"Error connecting to the database: {e}")
        return None