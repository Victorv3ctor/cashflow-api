from fastapi import Depends
from dependencies.db import get_db
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository

def get_account_repo(conn = Depends(get_db)):
    return AccountRepository(conn)

def get_transaction_repo(conn = Depends(get_db)):
    return TransactionRepository(conn)