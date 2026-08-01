from jose import jwt
from datetime import datetime,timedelta

SECRET_KEY="DivagarIsACulprit"
ALGORITHM="HS256"
EXIPRATION_IN_MINUTES=30

def generateToken(detail : dict):

    data=detail.copy()

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