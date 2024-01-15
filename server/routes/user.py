from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.utils.hash_password import (hash_password, compare_password)

from server.database import(
    create_user,
    retrieve_user,
    retrieve_users,
    update_users,
    delete_user
)

from server.models.users import(
    ErrorResponseModel,
    SuccessResponseModel,
    UserModel,
    UpdateUserModel,
)

router = APIRouter()

@router.get("/{id}", response_description="User data retrieved")
async def get_user_by_id(id):
    user = await retrieve_user(id)
    if user:
        return SuccessResponseModel(user, "User data fetched")
    return ErrorResponseModel("Error", 404, "User does not exist")

@router.post("/", response_description="creates a new user")
async def register(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = hash_password(user["password"])
    new_user = await create_user(user)
    return SuccessResponseModel(new_user, "User created successfully")
