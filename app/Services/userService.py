from fastapi import HTTPException
from app.Models.models import User
from app.Models.models import LoginRequest
from ..Database.database import user_collection
from ..utils.jwtconfig import generateToken

class userService:

    def userRegister(newUser:User):
            existing_user=user_collection.find_one({"user_email":newUser.user_email})
            if existing_user:
                raise HTTPException(status_code=400,detail="User already exists")
            user_collection.insert_one(newUser.model_dump())
            return {
                "message" : "Admin registered" if newUser.user_role=="admin" else "User registered",
                "user" : newUser
            }
    
    def userLogin(loginUser:LoginRequest):
        user=user_collection.find_one(
             {"user_email":loginUser.user_email}
        )
        if user is not None:
            if user["user_password"] == loginUser.user_password:
                #  return{
                #       "Message" : "User loggedIn"
                #  }

                token=generateToken(
                     {
                          "user_email":user["user_email"],
                          "user_role":user["user_role"]
                     }
                )

                return {
                     "message":"User loggedIn",
                     "token" : token
                }
            
            else:
                 raise HTTPException(status_code=400,detail="Email or password is invalid")
        else:
            return{
              "detail" : "Register before login"
              }
         
    def getAllUsers():
        users=list(user_collection.find())
        for user in users:
            user["_id"]=str(user["_id"])
        return users

         