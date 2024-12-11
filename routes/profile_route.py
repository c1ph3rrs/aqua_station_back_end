from fastapi import APIRouter, HTTPException
from model.profile import UpdateProfileRequest
from db_connection import user_collection
from bson import json_util
import json
from bson import ObjectId


router = APIRouter()

@router.put("/update/{phone}")
async def update_profile(phone: str, profile_data: UpdateProfileRequest):
    user = user_collection.find_one({"phone": phone})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    update_data = {
        "name": profile_data.name,
        "email": profile_data.email,
        "dob": profile_data.dob,
        "region": profile_data.region,
        "gender": profile_data.gender,
    }
    
    result = user_collection.update_one(
        {"phone": phone},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Profile update failed")
        
    updated_user = user_collection.find_one({"phone": phone})
    return json.loads(json_util.dumps(updated_user))


@router.get("/{phone}")
async def get_profile(phone: str):
    user = user_collection.find_one({"phone": phone})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return json.loads(json_util.dumps(user))


@router.get("/id/{user_id}")
async def get_profile_by_id(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Format the user data as required, using 'id' instead of '_id'
    formatted_user = {
        "id": str(user["_id"]),  # Directly assign the string representation of '_id' to 'id'
        "name": user.get("name"),
        "email": user.get("email"),
        "dob": user.get("dob"),
        "region": user.get("region"),
        "phone": user.get("phone"),
        "gender": user.get("gender"),
        "allow_notifications": user.get("allow_notifications"),
        "token": user.get("token", ""),
        "created_at": user.get("created_at"),
        "balance": float(user.get("balance", 0))
    }
    
    return formatted_user

@router.post("/add/token")
async def post_token(user_id: str, token: str):
    from bson import ObjectId

    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        return {"detail": "User not found"}

    tokens = user.get("tokens", [])
    if token in tokens:
        return {"detail": "Token already exists"}

    tokens.append(token)
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"tokens": tokens}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Token update failed")

    return {"detail": "Token added successfully"}


@router.delete("/remove/token")
async def remove_token(user_id: str, token: str):
    from bson import ObjectId

    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        return {"detail": "User not found"}

    tokens = user.get("tokens", [])
    if token not in tokens:
        return {"detail": "Token does not exist!"}

    tokens.remove(token)
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"tokens": tokens}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Token removal failed")

    return {"detail": "Token removed successfully"}
