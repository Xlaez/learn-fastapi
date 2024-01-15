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

@router.post("/", response_description="creates a new user")
async def register(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = hash_password(user["password"])
    new_user = await create_user(user)
    return SuccessResponseModel(new_user, "User created successfully")

@router.get("/all", response_description="Users fetched")
async def get_users():
    users = await retrieve_users()
    if users:
        return SuccessResponseModel(users, "Users data fetched")
    return ErrorResponseModel("Error", 404, "Database empty, there are no users yet")

@router.get("/{id}", response_description="User data retrieved")
async def get_user_by_id(id):
    user = await retrieve_user(id)
    if user:
        return SuccessResponseModel(user, "User data fetched")
    return ErrorResponseModel("Error", 404, "User does not exist")

@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_users(id, req)

    if updated_user:
        return SuccessResponseModel("User with ID: {} updated successfully".format(id), "Success")
    return ErrorResponseModel("Error", 400, "Cannot update user data")