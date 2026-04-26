import datetime

class Transaction:
    def __init__(self, t_id, amount, t_type, category, date):
        self.t_id = t_id
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.date = date or datetime.datetime.now()


