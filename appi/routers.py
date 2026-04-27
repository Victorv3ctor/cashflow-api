from fastapi import FastAPI, Depends, HTTPException

from models.schemas import RegisterRequest, LoginRequest, NewTransaction

from service.accountservice import AccountService
from service.transaction_service import TransactionService
from service.auth_service import AuthService

from dependencies.services import get_account_service, get_transaction_service
from dependencies.current_account import get_current_account
app = FastAPI()

@app.post('/register')
def register(
        data: RegisterRequest,
        service: AccountService = Depends(get_account_service)
):
    try:
        service.create_account(data.username, data.password, data.balance)
        return {'status': 'OK', 'message': 'ACCOUNT CREATED'}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.post('/login')
def login_in(
        data: LoginRequest,
        service: AccountService = Depends(get_account_service)
):
    account = service.verify_user_credentials(data.username, data.password)
    if account:
        token = AuthService.create_token(account.account_id)
        return {"access_token": token, "id": account.account_id}
    raise HTTPException(status_code=401, detail='WRONG USERNAME/PASSWORD')

@app.post('/transactions')
def add_transaction(
        data: NewTransaction, account=Depends(get_current_account),
        service: TransactionService = Depends(get_transaction_service)
):
    try:
        service.new_transaction(account.account_id, data.t_type, data.amount, data.category)
        return {"status": "OK", "message": "NEW TRANSACTION ADDED"}
    except ValueError:
        raise HTTPException(status_code=400, detail="WRONG TRANSACTION TYPE")

@app.get('/transactions')
def get_transactions(
        transaction_type: str | None = None, order_by: str | None = None,
        account=Depends(get_current_account),
        service: TransactionService = Depends(get_transaction_service)
):
    try:
        transactions = service.display_transactions(account.account_id, transaction_type, order_by)
        return {"status": "OK", "account_id": account.account_id, "transactions": transactions}
    except ValueError:
        raise HTTPException(status_code=400, detail="WRONG FILTER OPTION")

@app.get('/account')
def activity_status(
        service: TransactionService = Depends(get_transaction_service),
        account=Depends(get_current_account)
):
    stats = service.get_transaction_stats(account.account_id)
    return {
        "status": "OK",
        "account": account.username,
        "balance": account.balance,
        "statistics": stats,
    }

@app.delete('/transactions/{delete_id}')
def delete_transaction(
        delete_id: int, account=Depends(get_current_account),
        service: TransactionService = Depends(get_transaction_service)
):
    try:
        service.delete_transaction(account.account_id, delete_id)
        return {'status': 'OK', 'message': 'TRANSACTION DELETED'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
