from models.account import Account
#REPOSITORY NIE POWINNO OBSLUGIWAC COMMIT ROLLBACK BO LAMIE WTEDY MOZLIWOSC JEDNEJ
#TRANSAKCJI OBEJMUJACEJ WIELE ZAPYTAN
class AccountRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_account(self, username, str_hashed_pwd, balance):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        INSERT INTO account(username, password, balance) VALUES
            (%s, %s, %s)""", (username, str_hashed_pwd, balance))

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










