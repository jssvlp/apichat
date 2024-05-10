import sqlite3

database = "database/chats"

def get_connection():
    return sqlite3.connect(database)
    
def sql(query):
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as ex:
        print(ex)
