import hashlib
import re

from dotenv import dotenv_values
from fastapi import APIRouter, Request, HTTPException, Depends, Security
from pydantic import BaseModel

from ..jwt.Guard import validate_token
from ..jwt.Utils import JwtUtils
from ..user.User import User

ME = APIRouter()

config = dotenv_values(".env")


@ME.get("/me", response_description="Login User")
def me(token_data: dict = Depends(validate_token)):
    return token_data
