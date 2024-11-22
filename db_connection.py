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

    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"An error occurred while connecting to MongoDB: {e}")