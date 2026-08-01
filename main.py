from fastapi import FastAPI,HTTPException
from app.Database.database import db
from app.Routes.productRoutes import productRouter
from app.Routes.userRoutes import userRouter

app=FastAPI()
app.include_router(productRouter)
app.include_router(userRouter)