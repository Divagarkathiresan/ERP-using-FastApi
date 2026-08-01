from fastapi import APIRouter
from ..Database.database import user_collection
from ..Models.models import User
from ..Models.models import LoginRequest
from ..Services.userService import userService

userRouter=APIRouter()

class userRoute:

    @userRouter.post("/user/register",status_code=201)
    def addNewUser(user:User):
        return userService.userRegister(user)


    @userRouter.post("/user/login",status_code=200)
    def userLogin(loginUser:LoginRequest):
        return userService.userLogin(loginUser)
        

    @userRouter.get("/user",status_code=200)
    def getAllUsers():
        return userService.getAllUsers()
