from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from models.schemas import *
from services.accountservice import AccountService
from storage.db_storage import Database

load_dotenv()

storage = Database(
    os.getenv('DB_HOST'),
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_NAME')
)

security = HTTPBearer()
SECRET_KEY = os.getenv('JWT_SECURITY_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')

def create_token(account_id: int):
    payload = {
        "sub": str(account_id),
        "exp": datetime.now() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_account(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
    account = storage.display_account(account_id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

app = FastAPI()

@app.post('/register')
def register(data: RegisterRequest):
    account_service = AccountService(None, storage)
    result = account_service.new_account(data.username, data.password, data.balance)
    if result:
        return {"status": "OK", "message": "ACCOUNT CREATED"}
    return {"status": "ERROR", "message": "USERNAME ALREADY EXISTS. TRY AGAIN"}

@app.post('/login')
def login_in(data: LoginRequest):
    account_service = AccountService(None, storage)
    account = account_service.get_login_in(data.username, data.password)
    if account:
        token = create_token(account.account_id)
        return {"access_token": token}
    return {"status": "ERROR", "message": "WRONG USERNAME / PASSWORD. TRY AGAIN"}

@app.post('/transactions')
def new_transaction(data: NewTransaction, account=Depends(get_current_account)):
    service = AccountService(account, storage)
    result = service.new_transaction(data.t_type, data.amount, data.category)
    if not result:
        return {"status": "ERROR", "message": "TRANSACTION NOT ADDED"}
    return {"status": "OK", "message": "TRANSACTION ADDED"}

@app.get('/transactions')
def get_transactions(filtr_option: str | None = None, account=Depends(get_current_account)):
    service = AccountService(account, storage)
    transactions = service.filtr_transactions(filtr_option, order_by='date') if filtr_option else service.get_transactions_and_id()
    if not transactions:
        return {'status': 'ERROR', 'message': 'TRANSACTIONS NOT FOUND'}
    return {"status": "OK", "account": account.username, "transactions": transactions}

@app.get('/account')
def show_account_status(account=Depends(get_current_account)):
    service = AccountService(account, storage)
    transactions_count = service.get_transactions_count(account.account_id)
    stats = service.get_transaction_statistics()
    return {
        "status": "OK",
        "account": account.username,
        "balance": account.balance,
        "statistics": 0 if not stats else stats,
        "transactions total": transactions_count
    }

@app.delete('/transactions/{delete_id}')
def delete_transaction(delete_id: int, account=Depends(get_current_account)):
    service = AccountService(account, storage)
    result = service.delete_transaction_by_id(delete_id)
    if not result:
        return {'status': 'ERROR', 'message': 'TRANSACTION NOT FOUND'}
    return {'status': 'OK', 'message': 'TRANSACTION DELETED'}