import bcrypt

class AccountService:
    def __init__(self, account, storage):
        self.account = account
        self.storage = storage

    def new_account(self, username, password, balance):
        hashing_pwd = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt() #chaning user password to bytes, and hashing with salt
        )
        str_hashed_pw = hashing_pwd.decode('utf-8') # encoding hashed password to string for mySQL column
        return self.storage.create_account(username, str_hashed_pw, balance) # forward hashed string password

    def get_login_in(self, username, password):
        account = self.storage.display_account(username=username)
        if not account:
            return None
        hashed_password = account.password
        check = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        if check:
            return account
        return False

    def new_transaction(self, t_type, amount, category):
        account_id = self.account.get_account_id()
        t_type = t_type.upper()
        if t_type not in ['INCOME', 'EXPAND']:
            return None
        self.storage.add_transaction(account_id, amount, t_type, category)
        return True

    def filtr_transactions(self, filtr_option: str | None = None, order_by: str | None = None):
        account_id = self.account.get_account_id()
        if filtr_option is not None or order_by is not None:
            return self.storage.display_transactions(account_id, filtr_option, order_by)
        return self.storage.display_transactions(account_id)

    def get_transactions_count(self, account_id):
        return self.storage.count_transactions(account_id)

    def delete_transaction_by_id(self, choice):
        account_id = self.account.get_account_id()
        return self.storage.delete_transaction(choice, account_id)

    def get_transaction_statistics(self):
        account_id = self.account.get_account_id()
        return self.storage.display_transaction_statistics(account_id)