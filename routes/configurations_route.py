from fastapi import APIRouter, HTTPException
import json
from bson import json_util
from db_connection import prices_collection, user_points_collection

router = APIRouter()

@router.get("/water-price")
async def get_prices():
    price = prices_collection.find_one()
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    
    price["id"] = str(price["_id"])
    del price["_id"]
    
    return json.loads(json_util.dumps(price))

@router.get("/points/{user_id}")
async def get_user_points(user_id: str):
    user_points = user_points_collection.find_one({"user_id": user_id})
    
    if not user_points:
        raise HTTPException(status_code=404, detail="User points not found")
        
    user_points["id"] = str(user_points["_id"])
    del user_points["_id"]
    
    return json.loads(json_util.dumps(user_points))
