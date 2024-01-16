from fastapi import HTTPException, status
from dotenv import load_dotenv
import os
import motor.motor_asyncio
from datetime import datetime
from bson.objectid import ObjectId

load_dotenv()

database_url = os.getenv("MONGO_URL")
secret_key = os.getenv("SECRET_KEY")

client  = motor.motor_asyncio.AsyncIOMotorClient(database_url)

database = client.users

users_collection = database.get_collection("users")

def users_helper(users) -> dict:
    created_at_str = users.get("createdAt", "")

    if isinstance(created_at_str, datetime):
        created_at_datetime = created_at_str
    else:
        created_at_datetime = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")


    return{
        "id": str(users["_id"]),
        "fullname": users["fullname"],
        "email": users["email"],
        # "password": users["password"],
        "bio": users["bio"],
        "createdAt": created_at_datetime
    }

def users_helper_with_password(users) -> dict:
    created_at_str = users.get("createdAt", "")

    if isinstance(created_at_str, datetime):
        created_at_datetime = created_at_str
    else:
        created_at_datetime = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")


    return{
        "id": str(users["_id"]),
        "fullname": users["fullname"],
        "email": users["email"],
        "password": users["password"],
        "bio": users["bio"],
        "createdAt": created_at_datetime
    }

async def retrieve_users():
    """
    Retrieves all users present in the database
    """
    users = []
    async for user in users_collection.find():
        users.append(users_helper(user))
    return users

async def update_users(id: str, data: dict) -> bool:
    """
    Updates a user by the given Id
    Return False if an empty request body is sent.
    """
    if len(data) <1 :
        return False

    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_user:
            return True
        return False
    

async def retrieve_user(id:str) -> dict:
    """
    Retrieves a single user
    """
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        return users_helper(user)
    else:
        return {}
    

async def retrieve_user_email(email:str) -> dict:
    """
    Retrieves a single user
    """
    user = await users_collection.find_one({"email": email})
    if user:
        return users_helper_with_password(user)
    else:
        return {}
    
async def create_user(user_data: dict) -> dict:
    """
    Creates a new user and add to the database
    """

    user = await users_collection.find_one({"email": user_data["email"]})
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "email taken, try with another email or login")

    user_data["createdAt"] = datetime.utcnow()
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return users_helper(new_user)

async def delete_user(id: str) -> bool:
    """
    Delete a user
    """
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False