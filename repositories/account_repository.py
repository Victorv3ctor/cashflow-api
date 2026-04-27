from models.account import Account
from mysql.connector import IntegrityError

class AccountRepository:
    def __init__(self, conn):
        self.conn = conn


    def create_account(self, username, str_hashed_pwd, balance):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            INSERT INTO account(username, password, balance) VALUES
                (%s, %s, %s)""", (username, str_hashed_pwd, balance))
        except IntegrityError:
            raise ValueError("USERNAME ALREADY EXISTS")


    def get_by_account_by_id(self, account_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT account_id, username, password, balance
        FROM account WHERE account_id = %s """, (account_id,))

        row = cursor.fetchone()
        if row is None:
            return None
        return Account(row['account_id'], row['username'], row['password'], row['balance'])

    def get_user_by_username(self, username):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT account_id, username, password, balance
        FROM account WHERE username = %s """, (username,))

        row = cursor.fetchone()
        if not row:
            return None
        return Account(row['account_id'], row['username'], row['password'], row['balance'])










