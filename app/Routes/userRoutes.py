from fastapi import APIRouter
from ..Database.database import user_collection
from ..Models.models import User
from ..Services.userService import userService

userRouter=APIRouter()

class userRoute:

    @userRouter.post("/user",status_code=201)
    def addNewUser(user:User):
        return userService.userRegister(user)
        

    @userRouter.get("/user",status_code=200)
    def getAllUsers():
        return userService.getAllUsers()
