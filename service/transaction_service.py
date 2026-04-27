#main -> account_service -> database -> mysql # wydaje sie plaska, a moje pliki jak servic_account ma 7 funkcji troche myslacych wiec chyba warto rozbic na kolejna warstwe i zapewnic sobie
# czytelnosc i wiecej pola na logike ;)

#main -> transaction_service -> transaction_repository -> database -> mysql  #
from datetime import datetime

class TransactionService:
    def __init__(self, transaction_repo):
        self.transaction_repo = transaction_repo


    def new_transaction(self,account_id, transaction_type, amount, category):
        t_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_type = transaction_type.upper()
        if transaction_type not in ['INCOME', 'EXPAND']:
            raise ValueError
        self.transaction_repo.add_transaction(account_id, transaction_type, amount, category, t_date)
        self.transaction_repo.update_balance(amount if transaction_type =='INCOME' else -amount, account_id)

    def display_transactions(self, account_id, filtr_type, order_by):
        if filtr_type is not None and filtr_type.upper() not in ['INCOME', 'EXPAND']:
            raise ValueError
        if order_by is not None and order_by.upper() not in ['DATE', 'AMOUNT']:
            raise ValueError
        return self.transaction_repo.get_transactions(account_id, filtr_type, order_by)

    def get_transaction_stats(self, account_id):
        result =  self.transaction_repo.transaction_stats(account_id)
        if not result:
            return []
        return {r['t_type']: r['count'] for r in result}

    def delete_transaction(self, account_id, delete_id):
        transaction = self.transaction_repo.get_tranasction_by_id(account_id, delete_id)
        if not transaction:
            raise ValueError('TRANSACTION NOT FOUND')
        delta, t_type = transaction['amount'], transaction['t_type']
        deleted = self.transaction_repo.delete_transaction(account_id, delete_id)
        if deleted == 0:
            raise ValueError
        self.transaction_repo.update_balance(
            delta if t_type == 'INCOME' else -delta,
            account_id
        )








