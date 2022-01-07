from getpass import getpass
from mysql.connector import connect, Error



# A class to simplify common queries to the database
class Databases(object):
    
    def __init__(self, username: str, password: str, host: str):
        self.connection = connect(
        host=host,
        user=username,
        password=password,
    )
        
        
    def get_group(self, ID):
        try:
            with connect(
                host=host,
                user=username,
                password=password,
            ) as connection:
                create_db_query = "CREATE DATABASE online_movie_rating"
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query)
        except Error as e:
            print(e)
