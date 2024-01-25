from fastapi import APIRouter, HTTPException
from module.database import users_collection
import hashlib
from basemodel.login import UserLogin

router = APIRouter(
    tags=["User Authentication"],
    responses={404: {"description": "Not found"}}
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

@router.post("/login/")
async def login(user: UserLogin):
    # Find the user in the database
    user_data = users_collection.find_one({"username": user.username})

    if user_data and verify_password(user.password, user_data["password"]):
        # Extract user_id and username from user_data
        user_id = str(user_data.get("_id"))  # Assuming _id is used as user_id
        username = user_data.get("username")
        return {"user_id": user_id, "username": username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
