import mysql.connector
from config import Config

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    Remember to close the connection (and cursor) after use.
    """
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: '{err}' occurred")
        return None
