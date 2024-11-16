from fastapi import APIRouter, HTTPException, Depends
from model.common_model import PhoneNumberRequest, OTPRequest
from typing import Dict
import random

router = APIRouter()

# Mock database for storing OTPs
otp_db: Dict[str, int] = {}



def send_otp_to_phone(phone_number: str, otp: int):
    # Here you would integrate with a third-party service to send the OTP
    print(f"Sending OTP {otp} to phone number {phone_number}")

def generate_otp() -> int:
    return random.randint(100000, 999999)

def get_user_profile(phone_number: str) -> Dict:
    # Mock function to return user profile data
    return {
        "phone_number": phone_number,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

@router.post("/send-otp")
def send_otp(request: PhoneNumberRequest):
    otp = generate_otp()
    otp_db[request.phone_number] = otp
    send_otp_to_phone(request.phone_number, otp)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(request: OTPRequest):
    if request.phone_number not in otp_db or otp_db[request.phone_number] != request.otp:
        raise HTTPException(status_code=400, detail="OTP Invalid")
    
    # OTP is valid, remove it from the database
    del otp_db[request.phone_number]
    
    # Get user profile data
    user_profile = get_user_profile(request.phone_number)
    return user_profile
