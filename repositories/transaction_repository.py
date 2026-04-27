from models.transaction import Transaction

class TransactionRepository:
    def __init__(self, conn):
        self.conn = conn


    def add_transaction(self,account_id, t_type, amount, category, t_date):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        INSERT INTO transactions(account_id, t_type, amount, category, date)
            VALUES (%s, %s, %s, %s, %s)""", (account_id, t_type, amount, category, t_date))

    def get_transactions(self, account_id, transaction_type, order_by):
        cursor = self.conn.cursor(dictionary=True)
        query = """
                 SELECT t_id, amount, t_type, category, date
                 FROM transactions WHERE account_id = %s """

        params = [account_id]

        if transaction_type is not None:
            query += " AND t_type = %s"
            params.append(transaction_type)

        if order_by is not None:
            query += f" ORDER BY {order_by} DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [Transaction(**row) for row in rows]

    def transaction_stats(self, account_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT t_type, COUNT(*) as count
        FROM transactions WHERE account_id = %s GROUP BY t_type""", (account_id,))
        return cursor.fetchall()

    def get_tranasction_by_id(self, account_id, delete_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT t_id, amount, t_type, category, date FROM transactions 
        WHERE account_id = %s AND t_id = %s""",(account_id, delete_id))
        return cursor.fetchone()

    def update_balance(self, amount, account_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        UPDATE account 
        SET BALANCE = balance + %s 
        WHERE account_id = %s""", (amount, account_id))

    def delete_transaction(self, account_id, transaction_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        DELETE FROM transactions 
        WHERE account_id = %s AND t_id = %s""", (account_id, transaction_id))
        return cursor.rowcount



















