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
    
    otp_service = OTPService()
    otp_sent = otp_service.send_otp(phone, str(otp))
    
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
    
    del otp_db[phone]
    
    user = user_collection.find_one({"phone": phone})
    if user:
        user_dict = json.loads(json_util.dumps(user))
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
            "created_at": datetime.utcnow()
        }
        result = user_collection.insert_one(new_user)
        
        # Return the newly created user in JSON-serializable format
        created_user = user_collection.find_one({"_id": result.inserted_id})
        return json.loads(json_util.dumps(created_user))

