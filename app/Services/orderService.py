from fastapi import HTTPException,Depends
from ..Services.userService import userService
from ..Models.models import Orders
from ..Database.database import orderItem_collection,inventory_collection,orders_collection,product_collection
class orderService:

    def postOrders(orders : Orders):
        total_amount=0
        order_items=[]

        #order id generation
        order_id = "O" + str(orders_collection.count_documents({})+1)

        #retriving single item from the list of items
        for order in orders.items:

            #check order in the product section
            product_found = product_collection.find_one(
                {
                    "product_id" : order.product_id
                }
            )

            #handling the not found exception
            if product_found is None:
                raise HTTPException(status_code=404,detail=f"Product {order.product_id} not found ")

            #check inventory ( product available in the inventory )
            inventory_product_found=inventory_collection.find_one(
                {"product_id" : order.product_id}
            )

            if inventory_product_found is None:
                raise HTTPException(status_code=404,detail=f"Product {order.product_id} not found in the inventory ")

            #if available check quantity
            if inventory_product_found["quantity"] < order.quantity:
                raise HTTPException(status_code=400,detail="Insufficient quantity")

            order_amount=product_found["product_price"]*(order.quantity)
            total_amount+=order_amount

            #add item to order
            order_items.append(
                {
                    "product_id":order.product_id,
                    "quantity":order.quantity
                }
            )

            #if product and quantity is ok , then update the quantity in the inventory
            inventory_collection.update_one(
                {"product_id" : order.product_id},
                {
                    "$inc":{
                        "quantity" : -order.quantity
                    }
                }
            )

        order_list_dict={
            "order_id":order_id,
            "items":order_items,
            "total_amount":total_amount
        }

        orders_collection.insert_one(order_list_dict)

        return {
            "success": True,
            "message": "Order placed successfully",
            "order": {
                "order_id": order_list_dict["order_id"],
                "items": order_list_dict["items"],
                "total_amount": order_list_dict["total_amount"]
            }
        }             