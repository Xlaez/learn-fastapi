from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.utils.hash_password import (hash_password, compare_password)
from server.utils.auth_tokens import (generate_access_token, generate_refresh_token)

from server.database import(
    create_user,
    retrieve_user,
    retrieve_users,
    update_users,
    delete_user,
    retrieve_user_email
)

from server.models.users import(
    ErrorResponseModel,
    SuccessResponseModel,
    UserModel,
    UpdateUserModel,
    UserLoginModel
)

router = APIRouter()

@router.post("/register", response_description="creates a new user")
async def register(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user["password"] = hash_password(user["password"])
    new_user = await create_user(user)
    return SuccessResponseModel(new_user, "User created successfully")

@router.post("/signin", response_description="signin a new user")
async def login(user: UserLoginModel = Body(...)):
    present_user = await retrieve_user_email(jsonable_encoder(user)["email"])

    if len(present_user) ==0 :
        return ErrorResponseModel("Error", 400, "User not found, try signing up")
    if(compare_password(jsonable_encoder(user)["password"], present_user["password"])):
        access_token =  generate_access_token(present_user["id"])
        refresh_token = generate_refresh_token(present_user["id"])
    else:
        return ErrorResponseModel("Error",400, "login credentials incorrect")
    return SuccessResponseModel({"access_token": access_token, "refresh_token": refresh_token}, "User logged in successfully")

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

@router.delete("/{id}")
async def delete_user_data(id:str):
    deleted_user  = await delete_user(id)
    if deleted_user:
        return SuccessResponseModel("User with ID: {} deleted".format(id), "Successfully deleted user")
    ErrorResponseModel("Error", 400, "Cannot delete user from database")