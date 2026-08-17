from fastapi import FastAPI,HTTPException
from app.Database.database import db
from app.Routes.productRoutes import productRouter
from app.Routes.userRoutes import userRouter
from app.Routes.inventoryRoutes import inventoryRoute

app=FastAPI()
app.include_router(productRouter)
app.include_router(userRouter)
app.include_router(inventoryRoute.inventoryRouter)

