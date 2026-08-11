from fastapi import APIRouter,Body, Depends
from app.Services import userService
from ..Database.database import inventory_collection
from ..Models.models import Inventory
from ..Services.inventoryService import inventoryService
from ..Services.userService import userService

class inventoryRoute:

    inventoryRouter=APIRouter()

    @inventoryRouter.post("/inventory",status_code=201)
    def addNewInventory(inventory:Inventory,current_user=Depends(userService.getCurrentUser)):
        return inventoryService.addNewInventory(inventory,current_user)