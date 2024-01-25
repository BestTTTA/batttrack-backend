from fastapi import APIRouter, HTTPException
from module.database import users_collection
import hashlib
from basemodel.register import UserCreate

router = APIRouter(
    tags=["User Registration"],
    responses={404: {"description": "Not found"}}
)

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register/")
async def register_users(user_create: UserCreate):
    user_ids = []
    for user in user_create.users:
        # Check if username already exists
        if users_collection.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail=f"Username {user.username} already exists")

        # Hash the user's password
        hashed_password = hash_password(user.password)

        # Insert the new user into the database
        user_data = {"username": user.username, "password": hashed_password}
        result = users_collection.insert_one(user_data)

        # # Retrieve the MongoDB-generated ID and add to user_ids list
        # user_ids.append(str(result.inserted_id))

    return "Registered"