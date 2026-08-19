from jose import jwt
from datetime import datetime,timedelta
import bcrypt


SECRET_KEY="DivagarIsACulprit"
ALGORITHM="HS256"
EXIPRATION_IN_MINUTES=30

def generateToken(userDetail : dict):

    data=userDetail.copy()

    expire=datetime.utcnow() + timedelta(
        minutes=EXIPRATION_IN_MINUTES
    )

    data.update(
        {"exp":expire}
    )

    token=jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def decodeToken(token:str):
    
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM
    )

    return payload

def hashPassword(password:str):
    hashed_password=bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
    return hashed_password.decode("utf-8")

def verifyPassword(loginPassword : str, hashedPassword:str):
    return bcrypt.checkpw(
        loginPassword.encode("utf-8"),
        hashedPassword.encode("utf-8")
    )