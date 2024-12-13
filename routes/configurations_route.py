from fastapi import APIRouter, HTTPException
import json
from bson import json_util
from db_connection import prices_collection, user_points_collection, rewards_history_collection

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
        return {"user_id": user_id, "points": 0}
        
    user_points["id"] = str(user_points["_id"])
    del user_points["_id"]
    
    return json.loads(json_util.dumps(user_points))


@router.get("/rewards-history/{user_id}")
async def get_rewards_history(user_id: str):
    rewards_history = rewards_history_collection.find({"user_id": user_id})
    
    rewards_list = []
    for reward in rewards_history:
        reward["id"] = str(reward["_id"])
        reward["datetime"] = reward["datetime"].isoformat()  # Convert datetime to ISO format string
        del reward["_id"]
        rewards_list.append(json.loads(json_util.dumps(reward)))
    
    if not rewards_list:
        raise HTTPException(status_code=404, detail="Rewards history not found")
    
    return rewards_list


@router.get("/user-records/{user_id}")
async def get_user_records(user_id: str):
    user_points = user_points_collection.find_one({"user_id": user_id})
    
    if not user_points:
        raise HTTPException(status_code=404, detail="User points record not found")
    
    user_points["id"] = str(user_points["_id"])
    del user_points["_id"]
    
    return json.loads(json_util.dumps(user_points))
