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
        # Validate ObjectId
        try:
            user_id = ObjectId(transaction_request.user_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid user_id format.")

        print("Step 1: Valid user_id")

        payment_method = transaction_request.payment_method
        water_qty = transaction_request.water_qty
        use_points = transaction_request.use_points
        used_points = transaction_request.used_points
        machine_id = transaction_request.machine_id
        user_lat = transaction_request.user_lat
        user_lng = transaction_request.user_lng

        # Validate water quantity
        if water_qty <= 0 or water_qty % 5 != 0:
            raise HTTPException(
                status_code=400,
                detail="Water quantity must be greater than zero and a multiple of 5 liters (e.g., 5, 10, 15).",
            )

        print("Step 2: Valid water quantity")

        # Fetch user details
        user = user_collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        print("Step 3: User fetched successfully")

        # Use fixed water price per liter (0.15 AED)
        water_price_per_liter = 0.15

        print(f"Step 4: Water price per liter set to {water_price_per_liter} AED")

        # Points validation if used
        if use_points:
            user_points = user_points_collection.find_one({"user_id": user_id}) or {"total_points": 0}
            available_points = user_points.get("total_points", 0)
            if used_points > available_points:
                raise HTTPException(status_code=400, detail="Used points exceed available points.")
        else:
            available_points = 0

        print(f"Step 5: Available points: {available_points}")

        # Calculate total price
        total_price = water_qty * water_price_per_liter
        if use_points:
            discount = used_points / 100  # Each 100 points = 1 AED
            total_price -= discount

        if total_price < 0:
            total_price = 0
            status = "failed"
            remarks = "Transaction failed due to excessive points used."
        else:
            status = "success"
            remarks = None

        print(f"Step 6: Total price calculated: {total_price}, Status: {status}")

        # Generate unique transaction number
        transaction_number = generate_unique_transaction_number()

        print(f"Step 7: Transaction number generated: {transaction_number}")

        # Validate payment method
        if payment_method not in ["balance", "points", "balance-points"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid payment method. Must be 'balance', 'points', or 'balance-points'.",
            )

        # Check user balance
        if payment_method in ["balance", "balance-points"] and user.get("balance", 0) < total_price:
            raise HTTPException(status_code=400, detail="Insufficient balance.")

        print("Step 8: Payment method validated and balance checked")

        # Create transaction record
        transaction_record = {
            "user_id": str(user_id),
            "water_qty": water_qty,
            "transaction_number": transaction_number,
            "datetime": datetime.utcnow().timestamp(),
            "price": total_price,
            "total_amount": water_qty * water_price_per_liter,
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

        print(f"Step 9: Transaction record inserted: {transaction_record}")

        # Deduct points if used and transaction succeeded
        if use_points and status == "success":
            new_points = available_points - used_points
            user_points_collection.update_one(
                {"user_id": str(user_id)}, {"$set": {"total_points": new_points}}
            )
        else:
            new_points = available_points

        print(f"Step 10: Points updated if used: {new_points}")

        # Deduct balance if applicable
        if total_price > 0 and payment_method in ["balance", "balance-points"] and status == "success":
            new_balance = user.get("balance", 0) - total_price
            user_collection.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        else:
            new_balance = user.get("balance", 0)

        print(f"Step 11: Balance updated if applicable: {new_balance}")

    
        if status == "success":
            rewards_gained = int(total_price * 100) 
            user_points_collection.update_one(
                {"user_id": str(user_id)},
                {"$inc": {"total_points": rewards_gained}},
                upsert=True,
            )
            rewards_record = {
                "user_id": str(user_id),
                "points_changed": rewards_gained,
                "transaction_number": transaction_number,
                "datetime": datetime.utcnow(),
                "type": "gain",
            }
            rewards_history_collection.insert_one(rewards_record)

        return {
            "status": True,
            "message": "Transaction completed successfully",
            "transaction_number": transaction_number,
            "total_price": total_price,
            "new_balance": new_balance,
            "new_points": new_points,
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(traceback.format_exc())  
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")