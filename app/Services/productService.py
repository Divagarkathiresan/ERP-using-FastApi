from fastapi import HTTPException
from ..Database.database import product_collection
from ..Models.models import Product
from ..Models.models import User
from ..Database.database import product_collection
class productService:

    def addNewProduct(product : Product, current_user : User):
        if current_user["user_role"] == "admin":
            getExistingProductId=product_collection.find_one({
                "product_id" : product.product_id
            })
            if getExistingProductId is None:
                product_collection.insert_one(product.model_dump())
                return{
                    "Message" : "New product added",
                    "Product" : product
                }
            else:
                raise HTTPException(status_code=409,detail="Product already in the cart")
        else:
            raise HTTPException(status_code=401,detail="Only admins can add the products")

    def getAllProducts():
        products=list(product_collection.find({}))
        for product in products:
            product["_id"]=str(product["_id"])
        return products
