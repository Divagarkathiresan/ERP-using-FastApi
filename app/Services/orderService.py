from fastapi import HTTPException,Depends
from ..Services.userService import userService
from ..Models.models import Orders
from ..Database.database import inventory_collection,orders_collection,product_collection,invoice_collection
class orderService:

    def postOrders(orders : Orders):

        total_amount=0
        orders_list=[]

        #order id generation
        order_id = "Order - " + str(orders_collection.count_documents({})+1)

        orders_collection.insert_one(orders.model_dump())

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

            #single item and its price
            order_list_dict={
                "item":order.model_dump(),
                "sub_total":order_amount
            }

            #if product and quantity is ok , then update the quantity in the inventory
            inventory_collection.update_one(
                {"product_id" : order.product_id},
                {
                    "$inc":{
                        "quantity" : -order.quantity
                    }
                }
            ) 

            orders_list.append(
                order_list_dict
            )


        invoice_model_dict={
            "order_id":order_id,
            "orders":orders_list,
            "total_amount":total_amount
        }

        invoice_collection.insert_one(invoice_model_dict)

        return {
            "Sucess":True,
            "Message":"Order placed sucessfully",
            "Invoice":{
                "order_id":invoice_model_dict["order_id"],
                "orders":invoice_model_dict["orders"],
                "total_amount":invoice_model_dict["total_amount"]
            }
        }