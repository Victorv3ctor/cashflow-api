import mysql.connector
from models.account import Account
from models.transaction import Transaction
from datetime import datetime

class Database:
    def __init__(self, host, username, password, database):
        try:
            self.db = mysql.connector.connect(
                host=host,
                username=username,
                password=password,
                database=database
            )
            self.cursor = self.db.cursor()
        except Exception as err:
            print(err)

    def create_account(self, username, str_hashed_pw, balance):
        query = "INSERT INTO account (username, password, balance) VALUES (%s, %s, %s)"
        params = (username, str_hashed_pw, balance)
        try:
            self.cursor.execute(query, params)
            self.db.commit()
            return True
        except mysql.connector.errors.IntegrityError:
            return False

    def display_account(self, username: str | None = None, password: str | None = None, account_id: int | None = None):
        query = "SELECT * FROM account WHERE"
        params = []

        if username is not None:
            query += " username = %s"
            params.append(username)

        if username is not None and password is not None:
            query += " username = %s AND password = %s"
            params.extend([username, password])
        if account_id is not None:
            query += " account_id = %s"
            params.append(account_id)

        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        if row is None:
            return None
        account = Account(row[1], row[2], row[3])
        account.account_id = row[0]
        return account

    def add_transaction(self, account_id, amount, t_type, category):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            insert_query = "INSERT INTO transactions (account_id, amount, t_type, category, date) VALUES (%s, %s, %s, %s, %s)"
            insert_params = (account_id, amount, t_type, category, date)
            self.cursor.execute(insert_query, insert_params)
            update_query = "UPDATE account SET balance = balance + %s WHERE account_id = %s"
            update_params = (amount if t_type == 'INCOME' else -amount, account_id)
            self.cursor.execute(update_query, update_params)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f'Blad dodawania transakcji: {e}')
            return False

    def display_transactions(self, account_id, filtr_option: str | None = None, order_by: str | None = None):
        columns = "t_id, amount, t_type, category, date"
        query = f"SELECT {columns} FROM transactions WHERE account_id = %s"
        params = [account_id]
        if filtr_option is not None and filtr_option in ['income', 'expand']:
            query += " AND t_type = %s"
            params.append(filtr_option)
        if order_by is not None and order_by in ['date', 'amount']:
            query += f" ORDER BY {order_by} DESC"

        self.cursor.execute(query, params)

        rows = self.cursor.fetchall()
        transactions = []
        for row in rows:
            transaction = Transaction(row[1], row[2], row[3], row[0], row[4])
            transactions.append(transaction)
        return transactions

    def delete_transaction(self, delete_id: int, account_id: int):
        try:
            transaction_data_query = "SELECT amount, t_type FROM transactions WHERE t_id = %s and account_id = %s FOR UPDATE"
            transactions_data_params = (delete_id, account_id)
            self.cursor.execute(transaction_data_query, transactions_data_params)

            transaction_data = self.cursor.fetchone()
            if not transaction_data:
                return None

            amount, t_type = transaction_data

            delete_query = "DELETE FROM transactions WHERE t_id = %s and account_id = %s"
            delete_params = (delete_id, account_id)
            self.cursor.execute(delete_query, delete_params)

            update_query = "UPDATE account SET balance = balance + %s WHERE account_id = %s"
            update_params = (amount if t_type == 'EXPAND' else -amount, account_id)
            self.cursor.execute(update_query, update_params)

            self.db.commit()
            return True

        except Exception:
            self.db.rollback()
            return False

    def count_transactions(self, account_id):
        query = "SELECT COUNT(*) FROM transactions WHERE account_id = %s"
        params = (account_id,)
        self.cursor.execute(query, params)
        return self.cursor.fetchone()[0]

    def display_transaction_statistics(self, account_id):
        query = "SELECT SUM(amount), t_type FROM TRANSACTIONS WHERE account_id = %s GROUP BY t_type"
        data = (account_id,)
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return {r[1]: r[0] for r in result}