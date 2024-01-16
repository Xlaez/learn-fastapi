from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    fullname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    bio: str = Field(...)
    # createdAt: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Josh Edem",
                "email": "jsoh@edem.com",
                "bio": "I am a passionate web developer".format,
                "password": "somehashedpassword",
                # "createdAt": "2023-12-08 13:18:36.262078"
            }
        }


class UserLoginModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jsoh@edem.com",
                "password": "somehashedpassword",
            }
        }

class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[str]
    bio: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Josh Edem",
                "email": "jsohedem@gmail.com",
                "bio": "I am a passionate web developer".format,
            }
        }

def SuccessResponseModel(data, message):
    return{
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }

