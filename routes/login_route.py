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

    print(f"DB otp is ${otp_db}")
    print(f"Submited otp is {submitted_otp}")
    
    if phone not in otp_db:
        raise HTTPException(status_code=400, detail="No OTP was sent to this number")
    
    stored_otp = otp_db[phone]
    
    if submitted_otp != stored_otp:
        raise HTTPException(status_code=400, detail="OTP does not match")    
    
    user = user_collection.find_one({"phone": phone})

    if submitted_otp == stored_otp:
        del otp_db[phone]

    if user:
        user_dict = json.loads(json_util.dumps(user))
        user_dict["_id"] = str(user_dict["_id"]["$oid"])
        if user_dict.get("dob"):
            user_dict["dob"] = user_dict["dob"]["$date"]
        if user_dict.get("created_at"):
            user_dict["created_at"] = user_dict["created_at"]["$date"]
        return user_dict
    else:
        print("New User found")
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
        
        created_user = user_collection.find_one({"_id": result.inserted_id})
        return json.loads(json_util.dumps(created_user))

