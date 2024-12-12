from fastapi import APIRouter, HTTPException, Body
import random
import string
from datetime import datetime
from bson import ObjectId
from db_connection import user_collection, transactions_collection, prices_collection, user_points_collection, rewards_history_collection
from pydantic import BaseModel


router = APIRouter()


class TransactionRequest(BaseModel):
    user_id: str
    payment_method: str
    water_qty: int
    use_points: bool
    used_points: int = 0
    machine_id: str = None
    user_lat: float = None
    user_lng: float = None


def generate_unique_transaction_number():
    while True:
        transaction_number = "TX" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        if not transactions_collection.find_one({"transaction_number": transaction_number}):
            return transaction_number

@router.post("/transaction")
async def create_transaction(transaction_request: TransactionRequest):
    try:
        # Extract values from the transaction request
        user_id = transaction_request.user_id
        payment_method = transaction_request.payment_method
        water_qty = transaction_request.water_qty
        use_points = transaction_request.use_points
        used_points = transaction_request.used_points
        machine_id = transaction_request.machine_id
        user_lat = transaction_request.user_lat
        user_lng = transaction_request.user_lng

        if water_qty <= 0 or water_qty % 5 != 0:
            raise HTTPException(status_code=400, detail="Water quantity must be greater than zero and a multiple of 5 liters (e.g., 5, 10, 15).")
        
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Fetch price dynamically from prices_collection
        water_price_data = prices_collection.find_one()
        if not water_price_data or "price" not in water_price_data:
            raise HTTPException(status_code=500, detail="Water price data not found.")
        
        water_price_per_liter = water_price_data["price"] / 5  # Convert 5L price to per-liter price

        if use_points:
            user_points = user_points_collection.find_one({"user_id": ObjectId(user_id)}) or {"total_points": 0}
            available_points = user_points.get("total_points", 0)
            if used_points > available_points:
                raise HTTPException(status_code=400, detail="Used points exceed available points.")
        
        total_price = water_qty * water_price_per_liter
        if use_points:
            points_value = used_points * (water_price_per_liter / 10)  # Adjust value of each point
            total_price -= points_value
        
        if total_price < 0:
            total_price = 0
            status = "failed"
            remarks = "Transaction failed due to excessive points used."
        else:
            status = "success"
            remarks = None
        
        transaction_number = generate_unique_transaction_number()
        
        if payment_method not in ["balance", "points", "balance-points"]:
            raise HTTPException(status_code=400, detail="Invalid payment method. Must be 'balance', 'points', or 'balance-points'.")
        
        if payment_method in ["balance", "balance-points"] and user.get("balance", 0) < total_price:
            raise HTTPException(status_code=400, detail="Insufficient balance.")
        
        transaction_record = {
            "user_id": user_id,
            "water_qty": water_qty,
            "transaction_number": transaction_number,
            "datetime": datetime.utcnow(),
            "price": total_price,
            "use_points": use_points,
            "used_points": used_points,
            "water_price_per_liter": water_price_per_liter,
            "status": status,
            "transaction_type": "purchase",
            "payment_method": payment_method, 
            "machine_id": machine_id,  
            "remarks": remarks,
            "discounts_applied": [],  
            "tax": 0.0,
            "user_lat": user_lat,
            "user_lng": user_lng,
        }
        
        transactions_collection.insert_one(transaction_record)

        if use_points and status == "success":
            new_points = available_points - used_points
            user_points_collection.update_one({"user_id": ObjectId(user_id)}, {"$set": {"total_points": new_points}})

        if total_price > 0 and payment_method in ["balance", "balance-points"] and status == "success":
            new_balance = user.get("balance", 0) - total_price
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": new_balance}})

        if status == "success":
            rewards_gained = water_qty // 5  # 1 point for each 5L fill
            user_points_collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$inc": {"total_points": rewards_gained}},
                upsert=True
            )
            rewards_record = {
                "user_id": user_id,
                "points_changed": rewards_gained,
                "transaction_number": transaction_number,
                "datetime": datetime.utcnow(),
                "type": "gain"
            }
            rewards_history_collection.insert_one(rewards_record)

        return {
            "status": True,
            "message": "Transaction completed successfully",
            "transaction_number": transaction_number,
            "total_price": total_price,
            "new_balance": new_balance if total_price > 0 else user.get("balance", 0),
            "new_points": new_points if use_points else available_points
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")