from fastapi import APIRouter, HTTPException
import json
from bson import json_util
from aqua_station_back_end.db_connection import prices_collection, user_points_collection

router = APIRouter()

@router.get("/prices")
async def get_prices():
    prices = prices_collection.find()
    formatted_prices = []
    for price in prices:
        price["id"] = str(price["_id"])
        del price["_id"]
        formatted_prices.append(price)
    return json.loads(json_util.dumps(formatted_prices))

@router.get("/user_points/{user_id}")
async def get_user_points(user_id: str):
    user_points = user_points_collection.find_one({"user_id": user_id})
    
    if not user_points:
        raise HTTPException(status_code=404, detail="User points not found")
        
    user_points["id"] = str(user_points["_id"])
    del user_points["_id"]
    
    return json.loads(json_util.dumps(user_points))

