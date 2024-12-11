from fastapi import APIRouter, HTTPException, Depends
from services.otp_service import OTPService
from model.common_model import PhoneNumberRequest, OTPRequest
from db_connection import user_collection
from datetime import datetime
from typing import Optional
from bson import json_util
from typing import Dict
import json
import random

router = APIRouter()

otp_db: Dict[str, int] = {}



@router.post("/user")
async def send_otp(phone_request: PhoneNumberRequest):
    phone = phone_request.phone_number
    
    otp = 1234
    otp_db[phone] = otp
    
    user = user_collection.find_one({"phone": phone})
    
    # otp_service = OTPService()
    # otp_sent = otp_service.send_otp(phone, str(otp))

    otp_sent =  True
    
    if otp_sent:
        if user:
            return {"message": "OTP sent successfully", "is_existing_user": True}
        else:
            return {"message": "OTP sent successfully", "is_existing_user": False}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

@router.post("/verify-otp")
async def verify_otp(otp_request: OTPRequest):
    phone = otp_request.phone_number
    submitted_otp = otp_request.otp
    
    if phone not in otp_db:
        raise HTTPException(status_code=400, detail="No OTP was sent to this number")
    
    stored_otp = otp_db[phone]
    
    if submitted_otp != stored_otp:
        raise HTTPException(status_code=400, detail="OTP does not match")    
    
    user = user_collection.find_one({"phone": phone})

    if submitted_otp == stored_otp:
        del otp_db[phone]

    if user:
        user_dict = {
            "id": str(user["_id"]), 
            "name": user.get("name"),
            "email": user.get("email"),
            "dob": user.get("dob", None),  
            "region": user.get("region"),
            "phone": user.get("phone"),
            "gender": user.get("gender"),
            "allow_notifications": user.get("allow_notifications"),
            "token": user.get("token", ""),
            "created_at": user.get("created_at", None),  
            "balance": float(user.get("balance", 0))
        }
        return user_dict 
    else:
        new_user = {
            "name": "",
            "email": "",
            "dob": None,
            "region": "",
            "phone": phone,
            "gender": "",
            "allow_notifications": False,
            "token": "",
            "balance": 0,
            "created_at": datetime.utcnow()
        }
        result = user_collection.insert_one(new_user)
        
        created_user = user_collection.find_one({"_id": result.inserted_id})
        created_user_dict = json.loads(json_util.dumps(created_user))
        created_user_dict["id"] = str(created_user_dict["_id"])  # Change _id to id
        created_user_dict.pop("_id", None)  # Remove _id from the dictionary
        return created_user_dict
