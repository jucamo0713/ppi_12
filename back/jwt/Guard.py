from fastapi import Header, HTTPException

from .Utils import JwtUtils


def validate_token(authorization):
    print(authorization)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token type")
    token = authorization.split("Bearer ")[-1]
    return JwtUtils.decode_jwt_token(token)
