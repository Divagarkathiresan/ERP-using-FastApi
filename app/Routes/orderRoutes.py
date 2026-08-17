from fastapi import Depends,HTTPException,APIRouter
from app.Services.orderService import orderService
from app.Models.models import Orders

class orderRoute:
    orderRouter=APIRouter()
    
    @orderRouter.post("/order")
    def postOrder(items : Orders):
        return orderService.postOrders(items)