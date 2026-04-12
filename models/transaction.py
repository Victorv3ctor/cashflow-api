import datetime

class Transaction:
    def __init__(self, amount, t_type, category, t_id :None, date = None):
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.date = date or datetime.datetime.now()
        self.t_id = t_id

