from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
import random
import string
from datetime import datetime
from db_connection import user_collection, recharge_history_collection, notification_collection
import json

router = APIRouter()

class RechargeRequest(BaseModel):
    user_id: str
    recharge_amount: float

@router.post("/recharge")
async def recharge_user(request: RechargeRequest):
    user = user_collection.find_one({"_id": ObjectId(request.user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_balance = user.get("balance", 0.0)  
    
    bonus = 0.0  
    
    if request.recharge_amount >= 50:
        bonus = 5.0  

    recharge_number = "Rx" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    while recharge_history_collection.find_one({"recharge_number": recharge_number}):
        recharge_number = "Rx" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    new_balance = float(current_balance) + float(request.recharge_amount) + float(bonus)
    user_collection.update_one({"_id": ObjectId(request.user_id)}, {"$set": {"balance": new_balance}})

    recharge_record = {
        "user_id": request.user_id,
        "recharge_amount": request.recharge_amount,
        "bonus": bonus > 0,
        "bonus_amount": bonus,
        "datetime": datetime.now(),
        "recharge_number": recharge_number
    }
    recharge_history_collection.insert_one(recharge_record)

    notification_data = {
        "title": "Recharge Amount",
        "body": f"Congratulations you have recharged an amount of {request.recharge_amount} AED.",
        "icon": "",
        "user_id": request.user_id,
        "notification_datetime": datetime.now(),
        "data": json.dumps({"redirect_screen": "notifications", "notification_id": "Nf" + ''.join(random.choices(string.ascii_letters + string.digits, k=8)), "user_id": request.user_id})
    }
    notification_collection.insert_one(notification_data)

    if request.recharge_amount > 50:
        extra_notification_data = {
            "title": "Bonus Amount",
            "body": f"Congratulations you got 5 AED extra on recharge of {request.recharge_amount} AED or more.",
            "icon": "",
            "user_id": request.user_id,
            "notification_datetime": datetime.now(),
            "data": json.dumps({"redirect_screen": "notifications", "notification_id": "ENf" + ''.join(random.choices(string.ascii_letters + string.digits, k=8)), "user_id": request.user_id})
        }
        notification_collection.insert_one(extra_notification_data)
    
    return {
        "status": True,
        "message": "Recharge successful",
        "new_balance": new_balance,
        "recharge_number": recharge_number,
        "bonus": bonus > 0,
        "bonus_amount": bonus
    }




@router.get("/recharge/history/{user_id}")
async def get_recharge_history(user_id: str):
    recharge_history = list(recharge_history_collection.find({"user_id": user_id}))
    if not recharge_history:
        raise HTTPException(status_code=404, detail="No recharge history found for this user")
        
    # Format the recharge history to replace '_id' with 'id'
    formatted_history = []
    for record in recharge_history:
        record["id"] = str(record["_id"]) 
        record.pop("_id", None)  
        formatted_history.append(record)
        
    return formatted_history

