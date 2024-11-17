from fastapi import APIRouter, HTTPException
from model.profile import UpdateProfileRequest
from db_connection import user_collection
from bson import json_util
import json
from typing import Optional
from datetime import datetime

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
        "allow_notifications": profile_data.allow_notifications
    }
    
    result = user_collection.update_one(
        {"phone": phone},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Profile update failed")
        
    updated_user = user_collection.find_one({"phone": phone})
    return json.loads(json_util.dumps(updated_user))
