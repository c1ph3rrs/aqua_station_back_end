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