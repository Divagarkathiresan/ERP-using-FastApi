from fastapi import HTTPException
from app.Models.models import User
from ..Database.database import user_collection

class userService:
    def userRegister(newUser:User):
            existing_users=list(user_collection.find())
            for user in existing_users:
                if user["user_email"] == newUser.user_email:
                    return HTTPException(status_code=400, detail="Email already exists")
            user_collection.insert_one(newUser.model_dump())
            return {
                    "message":"User added" if newUser.user_role=="user" else "Admin added",
                    "user":newUser
                }

    def getAllUsers():
        users=list(user_collection.find())
        for user in users:
            user["_id"]=str(user["_id"])
        return users