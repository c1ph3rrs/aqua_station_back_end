from model.common_model import BaseModel
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    address: str
    latitude: float
    longitude: float

class InventoryItem(BaseModel):
    item_name: str
    quantity: int
    price: float

class Earnings(BaseModel):
    total: float
    currency: str = "RUB"  # Default to Russian Ruble

class VendingMachine(BaseModel):
    machine_id: str
    location: Location
    status: str = "active"
    inventory: List[InventoryItem]
    last_serviced: Optional[datetime]
    installation_date: datetime
    earnings: Earnings