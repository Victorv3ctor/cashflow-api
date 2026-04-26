import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error
from contextlib import contextmanager

class Database:
    def __init__(self):
        load_dotenv()
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        }
    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            raise RuntimeError(f"Database connection error: {e}")

    @contextmanager # pozwala stworzyc wlasny blok with np. with db.transaction() as conn:
    def transaction(self):
        conn = self.get_connection() # conn zwraca polaczenie z baza
        try:
            yield conn # oddaje kontrole do bloku with i daje uzytkownikowi conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
