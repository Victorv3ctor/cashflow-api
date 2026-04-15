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
    try:
        account_service.new_account(data.username, data.password, data.balance)
        return {'status': 'OK', 'message': 'ACCOUNT CREATED'}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/login')
def login_in(data: LoginRequest):
    account_service = AccountService(None, storage)
    account = account_service.verify_user_credentials(data.username, data.password)
    if account:
        token = create_token(account.account_id)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail='WRONG PASSWORD/USERNAME')

@app.post('/transactions')
def add_transaction(data: NewTransaction, account=Depends(get_current_account)):
    service = AccountService(account, storage)
    try:
        service.new_transaction(data.t_type, data.amount, data.category)
        return {"status": "OK", "message": "NEW TRANSACTION ADDED"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/transactions')
def get_transactions(filtr_option: str | None = None, order_by: str | None = None, account=Depends(get_current_account)):
    service = AccountService(account, storage)
    try:
        transactions = service.filtr_transactions(filtr_option, order_by)
        return {"status": "OK", "account": account.username, "transactions": transactions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    try:
        service.delete_transaction_by_id(delete_id)
        return {'status': 'OK', 'message': 'TRANSACTION DELETED'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
