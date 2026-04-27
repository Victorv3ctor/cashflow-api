from datetime import datetime
from datetime import timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECURITY_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')

class AuthService:

    @staticmethod
    def create_token(account_id: int):
        payload = {
            "sub": str(account_id),
            "exp": datetime.now() + timedelta(hours=2)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



