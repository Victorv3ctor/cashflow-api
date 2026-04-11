from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, description="Username must be at least 3 characters")
    password: str = Field(min_length=3, description="Password must be at least 3 characters")
    balance: int = Field(ge=0, description="Balance must be bigger or equal 0")

class LoginRequest(BaseModel):
    username: str
    password: str

class NewTransaction(BaseModel):
    t_type : str = Field(min_length = 3, description = "Transaction type must be at least 3 characters")
    amount: int = Field(ge=1, description="Amount must be bigger than 0")
    category: str = Field(min_length = 2, description="Category must be at least 3 characters")



