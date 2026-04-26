from fastapi import Depends
from dependencies.repos import get_account_repo
from dependencies.repos import get_transaction_repo
from service.accountservice import AccountService
from service.transaction_service import TransactionService

def get_account_service(account_repo = Depends(get_account_repo)):
    return AccountService(account_repo)

def get_transaction_service(transaction_repo = Depends(get_transaction_repo)):
    return TransactionService(transaction_repo)