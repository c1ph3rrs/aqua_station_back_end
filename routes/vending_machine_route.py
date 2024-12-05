from fastapi import APIRouter, HTTPException
from model.vending_machine_model import VendingMachine
from datetime import datetime
from db_connection import vending_machine_collection, machine_loc_collection
from bson import json_util
import json

router = APIRouter()


@router.post("/add")
async def add_vending_machine(machine: VendingMachine):
    existing = vending_machine_collection.find_one({"machine_id": machine.machine_id})
    if existing:
        raise HTTPException(status_code=400, detail="Machine ID already exists")
    
    machine_dict = machine.dict()
    result = vending_machine_collection.insert_one(machine_dict)
    
    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Failed to add vending machine")
        
    return {"message": "Vending machine added successfully", "id": str(result.inserted_id)}

@router.put("/{machine_id}")
async def update_vending_machine(machine_id: str, machine: VendingMachine):
    existing = vending_machine_collection.find_one({"machine_id": machine_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Vending machine not found")
    
    machine_dict = machine.dict()
    result = vending_machine_collection.update_one(
        {"machine_id": machine_id},
        {"$set": machine_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
        
    updated_machine = vending_machine_collection.find_one({"machine_id": machine_id})
    return json.loads(json_util.dumps(updated_machine))

@router.delete("/{machine_id}")
async def delete_vending_machine(machine_id: str):
    result = vending_machine_collection.delete_one({"machine_id": machine_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vending machine not found")
        
    return {"message": "Vending machine deleted successfully"}

@router.get("/{machine_id}")
async def get_vending_machine(machine_id: str):
    machine = vending_machine_collection.find_one({"machine_id": machine_id})
    
    if not machine:
        raise HTTPException(status_code=404, detail="Vending machine not found")
        
    return json.loads(json_util.dumps(machine))

@router.get("/all")
async def get_all_vending_machines():
    machines = vending_machine_collection.find()
    return json.loads(json_util.dumps(list(machines)))


@router.get("/loc/all")
async def get_all_machine_locations():
    locations = machine_loc_collection.find()
    formatted_locations = []
    for location in locations:
        location["id"] = str(location["_id"]) 
        del location["_id"] 
        formatted_locations.append(location)
    return formatted_locations