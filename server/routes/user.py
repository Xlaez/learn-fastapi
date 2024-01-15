from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

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