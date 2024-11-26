import firebase_admin
from firebase_admin import credentials
import requests
import json


def getAccessKey():

    cred = credentials.Certificate("whisper-crm-firebase-adminsdk-o5o2e-5dbb94200c.json")
    print(cred.get_access_token().access_token)
    return cred.get_access_token().access_token
    # firebase_admin.initialize_app(cred)



def send_notification():

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {getAccessKey()}'
    }

    url = "https://fcm.googleapis.com/v1/projects/whisper-crm/messages:send"

    payload = json.dumps({
            "message": {
                "token": "cpDdAarGTxaqqttGTq677o:APA91bFR2BM914X3JoHod92Ak58_CcKbnS0y4hWORfsXslOYJO-4vAhCppnYpZD7UWjjEc0G7ftYe06SSSbolyV_u2fh0alr_f1jQh9vOyf-XToMex7KGZI",
                "notification": {
                "body": "This is a Firebase Cloud Messaging Topic Message!",
                "title": "FCM Message"
                }
            }})
        
    print(f"Headers is {headers}")
    

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        print(f"Response is {response.json}")
    else:
        print(f"Response is {response}")


if __name__ == "__main__":
    send_notification()