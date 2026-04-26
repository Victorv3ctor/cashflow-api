from fastapi import Depends
from service.auth_service import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from dependencies.services import get_account_service
from service.accountservice import AccountService
from dotenv import load_dotenv
from jose import JWTError
import os


load_dotenv()

security = HTTPBearer() # robi całą robotę z wyciągnięciem i wstępną walidacją tokena
#z Authorization, jesli cos jest nie tak z tokenem zwraca odrazu 401

#HTTPAuthorizationCredentials ustandaryzowany sposob zwrotu wyniku (czyli opakowanie w obiekt)
#dlatego token wyciagamy z credentials.credentials

SECRET_KEY = os.getenv('JWT_SECURITY_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')

def get_current_account(
        credentials: HTTPAuthorizationCredentials=Depends(security),
        service: AccountService=Depends(get_account_service)
):
    try:
        token = credentials.credentials
        payload = AuthService.decode_token(token)
        account_id = int(payload.get("sub"))
        return service.get_account_by_id(account_id)
    except JWTError:
        raise HTTPException(status_code=401, detail='INVALID TOKEN')


