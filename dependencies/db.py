from storage.db_storage import Database

db = Database()

def get_db():
    with db.transaction() as conn:
        yield conn