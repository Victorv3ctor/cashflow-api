import bcrypt

class AccountService:
    def __init__(self, account_repo):
        self.account_repo = account_repo


    def create_account(self,username, password, balance):
        hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        str_hashed_pwd = hash_pwd.decode('utf-8')
        self.account_repo.create_account(username, str_hashed_pwd, balance)

    def verify_user_credentials(self, username, password):
        account = self.account_repo.get_user_by_username(username)
        if not account:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
            return account
        return False

    def get_account_by_id(self, account_id):
        return self.account_repo.get_by_account_by_id(account_id)

