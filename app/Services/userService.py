from fastapi import Depends,HTTPException
from app.Models.models import User
from app.Models.models import LoginRequest
from ..Database.database import user_collection
from ..utils.jwtconfig import *
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
class userService:

    def userRegister(newUser:User):
            existing_user=user_collection.find_one({"user_email":newUser.user_email})
            if existing_user:
                raise HTTPException(status_code=400,detail="User already exists")
            user_collection.insert_one(newUser.model_dump())
            return {
                "message" : "Admin registered" if newUser.user_role=="admin" else "User registered",
                "user" : {
                    "Id" : newUser.user_id,
                    "User name":newUser.user_name,
                    "Email" : newUser.user_email
                }
            }
    
    def userLogin(loginUser:LoginRequest):
        user=user_collection.find_one(
             {"user_email":loginUser.user_email}
        )
        if user is not None:
            if user["user_password"] == loginUser.user_password:

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


    def getCurrentUser(token:str = Depends(oauth2_scheme)):
        try:
            payload = decodeToken(token)
            user_email = payload.get("user_email")

            if user_email is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
            )
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        user = user_collection.find_one(
            {
                "user_email": user_email
            }
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        user["_id"]=str(user["_id"])
        return user