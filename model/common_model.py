from pydantic import BaseModel

class PhoneNumberRequest(BaseModel):
    phone_number: str

class OTPRequest(BaseModel):
    phone_number: str
    otp: int