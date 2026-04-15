import bcrypt
import mysql.connector

class AccountService:
    def __init__(self, account, storage):
        self.account = account
        self.storage = storage

    def new_account(self, username, password, balance):
        hashing_pwd = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt() #chaning user password to bytes, and hashing with salt
        )
        str_hashed_pw = hashing_pwd.decode('utf-8')
        # encoding hashed password to string for mySQL column
        try:
            self.storage.create_account(username, str_hashed_pw, balance)# forward hashed string password
        except mysql.connector.errors.IntegrityError:
            raise ValueError("USERNAME ALREADY EXISTS")
        except Exception:
            raise

    def verify_user_credentials(self, username, password): #proba dopasowania danych podanych przez usera
        #return None jest normalny, funkcja nie tworzy, nie dodaje
        account = self.storage.display_account(username=username)
        if not account:
            return None
        hashed_password = account.password
        check = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        if not check:
            return None
        return account

    def new_transaction(self, t_type, amount, category):
        account_id = self.account.get_account_id()
        t_type = t_type.upper()

        if t_type not in ['INCOME', 'EXPAND']:
            raise ValueError('WRONG TRANSACTION TYPE USED')

        self.storage.add_transaction(account_id, amount, t_type, category)

    def filtr_transactions(self, filtr_option: str | None = None, order_by: str | None = None):
        account_id = self.account.get_account_id()
        if filtr_option is not None and filtr_option not in ['income', 'expand']:
            raise ValueError('FILTR OPTIONS -> INCOME / EXPAND')
        if order_by is not None and order_by not in ['date', 'amount']:
            raise ValueError('FILTR BY -> date / amount')
        return self.storage.display_transactions(account_id, filtr_option, order_by)

    def get_transactions_count(self, account_id):
        return self.storage.count_transactions(account_id)

    def delete_transaction_by_id(self, delete_id):
        account_id = self.account.get_account_id()
        result = self.storage.delete_transaction(delete_id, account_id)
        if result is None:
            raise ValueError('TRANSACTION ID NOT FOUND')

    def get_transaction_statistics(self):
        account_id = self.account.get_account_id()
        return self.storage.display_transaction_statistics(account_id)