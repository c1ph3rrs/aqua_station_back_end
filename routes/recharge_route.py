from fastapi import APIRouter, HTTPException
import random
import string
from datetime import datetime
from db_connection import user_collection, recharge_history_collection

router = APIRouter()

@router.post("/recharge/{user_id}")
async def recharge_user(user_id: str, recharge_amount: float):
    user = user_collection.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_balance = user.get("balance", 0)
    
    if current_balance < 0:
        raise HTTPException(status_code=400, detail="Insufficient balance to recharge")
    
    new_balance = current_balance + recharge_amount
    user_collection.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
    
    while True:
        recharge_number = "Rx" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not recharge_history_collection.find_one({"recharge_number": recharge_number}):
            break
    
    recharge_record = {
        "user_id": user_id,
        "recharge_amount": recharge_amount,
        "datetime": datetime.now(),
        "recharge_number": recharge_number
    }
    recharge_history_collection.insert_one(recharge_record)
    
    return {
        "message": "Recharge successful",
        "new_balance": new_balance,
        "recharge_number": recharge_number
    }


@router.get("/recharge/history/{user_id}")
async def get_recharge_history(user_id: str):
    recharge_history = list(recharge_history_collection.find({"user_id": user_id}))
    if not recharge_history:
        raise HTTPException(status_code=404, detail="No recharge history found for this user")
        
    return  recharge_history

