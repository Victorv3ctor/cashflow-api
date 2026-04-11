class AccountService:
    def __init__(self, account, storage):
        self.account = account
        self.storage = storage

    def new_account(self, username, password, balance):
        return self.storage.create_account(username, password, balance)

    def get_login_in(self, username, password):
        return self.storage.display_account(username=username, password=password)

    def new_transaction(self, t_type, amount, category):
        account_id = self.account.get_account_id()
        t_type = t_type.upper()
        if t_type not in ['INCOME', 'EXPAND']:
            return None
        self.storage.add_transaction(account_id, amount, t_type, category)
        return True

    def filtr_transactions(self, filtr_option: str, order_by: str | None = None):
        account_id = self.account.get_account_id()
        params = []
        filtr_option = filtr_option.upper()
        if filtr_option not in ['INCOME', 'EXPAND']:
            return None
        params.append(filtr_option)
        if order_by is not None and order_by not in ['date', 'amount']:
            return None
        params.append(order_by)
        return self.storage.display_transactions(account_id, filtr_option, order_by, include_id=True)

    def get_transactions_count(self, account_id):
        return self.storage.count_transactions(account_id)

    def get_transactions_and_id(self):
        account_id = self.account.get_account_id()
        return self.storage.display_transactions(account_id, include_id=True)

    def delete_transaction_by_id(self, choice):
        account_id = self.account.get_account_id()
        return self.storage.delete_transaction(choice, account_id)

    def get_transaction_statistics(self):
        account_id = self.account.get_account_id()
        return self.storage.display_transaction_statistics(account_id)