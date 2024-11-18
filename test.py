import hmac
import hashlib
import time
import requests

# Configuration
BASE_URL = "https://dev-mobile.api.alivewater.online"
SERVICE_ID = "halyk"
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ENDPOINT = "/devices"

def generate_hash(service_id, dt, uri, body, secret_key):
    """
    Generate the hash signature for the API request.
    """
    data_to_sign = f"{service_id}{dt}{uri}{body}"
    signature = hmac.new(
        secret_key.encode('utf-8'),
        data_to_sign.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    return signature

def list_devices():
    """
    Make the API request to list devices.
    """
    # Current POSIX time
    dt = str(int(time.time()))

    # Request body (empty for GET requests)
    body = ""

    # Generate hash signature
    hash_signature = generate_hash(SERVICE_ID, dt, ENDPOINT, body, SECRET_KEY)

    # HTTP headers
    headers = {
        "Content-Type": "application/json",
        "hash": hash_signature,
        "serviceId": SERVICE_ID,
        "dt": dt
    }

    # Make GET request
    url = f"{BASE_URL}{ENDPOINT}"
    response = requests.get(url, headers=headers)

    # Return the response data
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Call the function
if __name__ == "__main__":
    devices = list_devices()
    print("Devices Listing:")
    print(devices)
