from fastapi import APIRouter,HTTPException
from ..Database.database import product_collection
from ..Models.models import Product
from bson import ObjectId

productRouter = APIRouter()

@productRouter.post("/product", status_code=201)
def addNewProduct(product : Product):
    product_collection.insert_one(product.model_dump())
    return {
        "message" : "Product added",
        "product" : product
    }

@productRouter.get("/product",status_code=200)
def getAllProducts():
    products=list(product_collection.find())
    for product in products:
        product["_id"]=str(product["_id"])
    return products

@productRouter.get("/product/{id}",status_code=200)
def getSingleProduct(id : str):
    product=product_collection.find_one(
        { "_id" : ObjectId(id)}
    )
    if product is not None:
        product["_id"]=str(product["_id"])
        return product
    else:
        raise HTTPException(status_code=404,detail="Product not found")

@productRouter.put("/product/{id}")
def updateSingleProduct(id:str,updateProduct:Product):
    product=product_collection.update_one(
        {"_id" : ObjectId(id)},
        {"$set" : updateProduct.model_dump()}
    )

    if product.modified_count == 0:
        raise HTTPException(status_code=200,detail="No data updated")
    else:
        return {
            "Message":"Data updated",
            "Updated Product":updateProduct
        }

@productRouter.delete("/product/{id}")
def deleteSingleProduct(id:str):
    result=product_collection.delete_one(
        {"_id":ObjectId(id)}
    )

    if result.deleted_count==0:
        raise HTTPException(status_code=200,detail="No data deleted")
    else:
        return {"Message" : "Data deleted"}

#pagination
@productRouter.get("/products/pagination")
def getProductsPageWise(page:int=1,limit:int=5):
    skip=(page-1)*limit
    products=list(product_collection.find().skip(skip).limit(limit))
    for product in products:
        product["_id"]=str(product["_id"])

    total_items=len(list(product_collection.find()))

    return {
        "products":products,
        "page":page,
        "limit":limit,
        "total":total_items,
        "next count": total_items - (page*limit) if total_items - (page*limit) > 0 else 0
    }

#filter
@productRouter.get("/products/filter")
def getProductsByCategory(category:str):
    productsCategoryWise=list(product_collection.find(
        {"product_category":category}
    ))
    for product in productsCategoryWise:
        product["_id"]=str(product["_id"])
    return productsCategoryWise

#sorting
@productRouter.get("/products/sort")
def getProductsSortedByPrice(order:str="asc",sorting:str="product_price"):
    sort_order=1 if order=="asc" else -1
    productsSortedByPrice=list(product_collection.find().sort(sorting,sort_order))
    for product in productsSortedByPrice:
        product["_id"]=str(product["_id"])
    return productsSortedByPrice