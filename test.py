import hmac
import hashlib
import time
import requests
import json
from db_connection import machine_loc_collection

# Configuration
BASE_URL = "https://dev-mobile.api.alivewater.online"
SERVICE_ID = "halyk"
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ENDPOINT = "/devices"

def generate_hash(service_id, dt, uri, body, secret_key):
    data_to_sign = f"{service_id}{dt}{uri}{body}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        data_to_sign.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    return signature

def list_devices():

    dt = str(int(time.time()))
    body = ""

    hash_signature = generate_hash(SERVICE_ID, dt, ENDPOINT, body, SECRET_KEY)


    headers = {
        "Content-Type": "application/json",
        "hash": hash_signature,
        "serviceId": SERVICE_ID,
        "dt": dt
    }

    url = f"{BASE_URL}{ENDPOINT}"
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
    



def load_machines_to_mongodb():
    

    with open("machines_locations.json", "r") as file:
        machines_data = json.load(file)

    # Insert data into MongoDB
    if isinstance(machines_data, list):
        machine_loc_collection.insert_many(machines_data)
    else:
        print("Data is not in the expected format (list).")


if __name__ == "__main__":
    # devices = list_devices()
    # print("Devices Listing:")
    # print(devices)
    load_machines_to_mongodb()
