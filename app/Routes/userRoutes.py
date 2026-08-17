from fastapi import APIRouter,Body
from ..Database.database import user_collection
from ..Models.models import RegisterRequest
from ..Models.models import LoginRequest
from ..Services.userService import userService
from ..utils.jwtAndPasswordConfig import generateToken

userRouter=APIRouter()

class userRoute:

    @userRouter.post("/user/register",status_code=201)
    def addNewUser(user:RegisterRequest):
        return userService.userRegister(user)

    @userRouter.post("/user/login",status_code=200)
    def userLogin(loginUser:LoginRequest):
        return userService.userLogin(loginUser)
        
    @userRouter.get("/user",status_code=200)
    def getAllUsers():
        return userService.getAllUsers()