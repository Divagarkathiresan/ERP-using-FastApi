from fastapi import HTTPException
from ..Database.database import inventory_collection
from ..Models.models import Inventory
from ..Models.models import User

class inventoryService:

    def addNewInventory(inventory : Inventory, current_user : User):
        if current_user["user_role"] == "manager":
            getExistingInventoryId=inventory_collection.find_one({
                "inventory_id" : inventory.inventory_id
            })
            if getExistingInventoryId is None:
                inventory_collection.insert_one(inventory.model_dump())
                return{
                    "Message" : "New inventory added",
                    "Inventory" : inventory
                }
            else:
                raise HTTPException(status_code=409,detail="Inventory already in the cart")
        else:
            raise HTTPException(status_code=401,detail="Only managers can add the inventories")

    
        