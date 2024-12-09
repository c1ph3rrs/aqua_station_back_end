from pymongo import MongoClient
from pymongo.collection import Collection
import certifi

MONGO_URI = "mongodb+srv://ciphersdevelopers:Tlc2moltVnuuoAGL@maincluster.sg74d.mongodb.net/"
DATABASE_NAME = "aqua_station"



try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]
    
    user_collection: Collection = db["users"]
    # user_info_collection: Collection = db["user_info"]

    report_collection: Collection = db["reports"]
    # users_collection: Collection = db["users"]
    # properties_collection: Collection = db["properties"]
    vending_machine_collection: Collection = db['machines']
    machine_loc_collection: Collection = db["machines_locations"]

    user_points_collection: Collection = db["users_points"]
    prices_collection: Collection = db["prices"]

    recharge_history_collection: Collection = db["recharge_history"]
    transactions_collection: Collection = db["transactions"]

    rewards_history_collection: Collection = db["rewards_history"]

    notification_collection: Collection = db["notifications"]
    
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"An error occurred while connecting to MongoDB: {e}")