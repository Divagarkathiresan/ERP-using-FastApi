from fastapi import HTTPException
from ..Database.database import inventory_collection,product_collection
from ..Models.models import Inventory
from ..Models.models import User

class inventoryService:

    def addNewInventory(inventory : Inventory, current_user : User):
        if current_user["user_role"] == "manager":
            getExistingInventoryId=inventory_collection.find_one({
                "inventory_id" : inventory.inventory_id
            })
            getProductId=product_collection.find_one({
                "product_id":inventory.product_id
            })
            if getExistingInventoryId is None:
                if getProductId is not None:
                    inventory_collection.insert_one(inventory.model_dump())
                    return{
                        "Message" : "New inventory added",
                        "Inventory" : inventory
                    }
                else:
                    raise HTTPException(status_code=404,detail="Product not found")

            else:
                raise HTTPException(status_code=409,detail="Inventory already in the cart")
        else:
            raise HTTPException(status_code=401,detail="Only managers can add the inventories")


    def getAllInventories(current_user : User):
        if current_user["user_role"] == "manager":
            inventories=list(inventory_collection.find({}))
            for inventory in inventories:
                inventory["_id"]=str(inventory["_id"])
            return inventories
        else:
            raise HTTPException(status_code=401,detail="Only managers can see the inventories")

    def updateSingleInventory(id:str,updateInventory:Inventory):
        inventory=inventory_collection.update_one(
            {"inventory_id" : id},
            {"$set" : updateInventory.model_dump()}
        )

        if inventory.modified_count == 0:
            raise HTTPException(status_code=200,detail="No data updated")
        else:
            return {
                "Message":"Data updated",
                "Updated Inventory":updateInventory
            }

    def deleteSingleInventory(id:str,current_user:User):
        if current_user["user_role"] == "manager":
            result=inventory_collection.delete_one({
                "inventory_id":id
            })
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Inventory not found"
                )
            else:
                return{"message":"Inventory deleted"}
        
        else:
            return HTTPException(
                status_code=401,
                detail="Only managers can delete the inventory"
            )
        