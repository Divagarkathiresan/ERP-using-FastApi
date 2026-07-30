from pydantic import BaseModel

class Product(BaseModel):
    product_name : str
    product_price : int
    product_quantity : int
    product_category:str

