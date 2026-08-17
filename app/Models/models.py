from enum import unique
from typing import Literal
from pydantic import BaseModel

class Product(BaseModel):
    product_id:str
    product_name : str
    product_price : int
    product_category:str

class Inventory(BaseModel):
    inventory_id : str
    product_id : str
    quantity : int

class User(BaseModel):
    user_id:str
    user_name : str
    user_email : str 
    user_password : str
    user_role : Literal["admin","manager" ,"user"]="user"

#Register model
class RegisterRequest(BaseModel):
    user_name : str
    user_email : str 
    user_password : str
    user_role : Literal["admin","manager" ,"user"]="user"
    
#login model
class LoginRequest(BaseModel):
    user_email: str
    user_password: str

class OrderItem(BaseModel):
    product_id : str
    quantity : int

class Orders(BaseModel):
    items:list[OrderItem]

class OrderList(BaseModel):
    item : OrderItem
    sub_total:int
class invoice(BaseModel):
    order_id : str
    orders : list[OrderList]
    total_amount : int