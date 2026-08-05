from enum import unique
from typing import Literal
from pydantic import BaseModel

class Product(BaseModel):
    product_id:str
    product_name : str
    product_price : int
    product_quantity : int
    product_category:str

class User(BaseModel):
    user_id:str
    user_name : str
    user_email : str 
    user_password : str
    user_role : Literal["admin", "user"]="user"

#login model
class LoginRequest(BaseModel):
    user_email: str
    user_password: str