from fastapi import FastAPI,HTTPException
from app.database import db
from app.routes import router

app=FastAPI()
app.include_router(router)