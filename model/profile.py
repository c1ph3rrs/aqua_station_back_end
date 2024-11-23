from model.common_model import BaseModel
from typing import Optional
from datetime import datetime

class UpdateProfileRequest(BaseModel):
    name: str
    email: str 
    dob: Optional[datetime]
    region: str
    gender: str
    allow_notifications: bool


class UserProfile(BaseModel):
    name: str
    email: str
    dob: Optional[datetime]
    region: str
    phone: str
    gender: str
    allow_notifications: bool
    token: str
    created_at: datetime
