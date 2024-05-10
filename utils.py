import mimetypes
import connection
import chats
import json

def get_mimetype(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype

def paginate_json(json_data, page_size):
    """
    Paginates JSON data into chunks of specified size.
    
    Args:
    json_data (list or dict): JSON data to paginate.
    page_size (int): Size of each page.
    
    Returns:
    list of dicts: Paginated JSON data.
    """
    if isinstance(json_data, dict):
        json_data = list(json_data.values())  # Convert dict to list of values
    
    return [json_data[i:i+page_size] for i in range(0, len(json_data), page_size)]

def load_chats_to_database():
    data = chats.getFromJson()
    counter = 0
    for  message in data['messages']:
        insert_message(message)
        counter = counter + 1
        print(f"Message {counter}/{len(data['messages'])} inserted.")



def insert_message(message):
    try:
        db_connection =  connection.get_connection()
        cursor = db_connection.cursor()
        sql = '''INSERT INTO messages (date, media, message, user) VALUES(?,?,?,?);'''

        data = (message['date'], json.dumps(message['media']),message['message'],message['user'])

        cursor.execute( sql,data)
        db_connection.commit()
        cursor.close()


    except Exception as ex:
        print(ex)
        print(message)
    ##'{message['date']}','{message['media']}','{message['message']}','{message['user']}'


if __name__ == "__main__":
    load_chats_to_database()