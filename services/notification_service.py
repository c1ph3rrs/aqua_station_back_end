import firebase_admin
from firebase_admin import credentials
import requests
import json


def initialize_firebase():
    try:
        cred = credentials.Certificate("al-marmoom-firebase-adminsdk-bmm2p-134b561456.json")
        firebase_admin.initialize_app(cred)
        return cred.get_access_token().access_token
    except Exception as e:
        raise Exception(f"Failed to initialize Firebase: {str(e)}")


def send_notification(token, title, body):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {initialize_firebase()}'
        }

        url = "https://fcm.googleapis.com/v1/projects/al-marmoom/messages:send"

        payload = json.dumps({
            "message": {
                "token": token,
                "notification": {
                    "body": body,
                    "title": title
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send notification: {str(e)}")


if __name__ == "__main__":
    test_token = "c4ioSUF-QLCDlimEO64tFb:APA91bERyKHNXIQr3G54sBPmPjknyNMEPIjQZpKWjyd3UdnUlQyLC5SkOUOLsFLs-l7HC_hT4jt-Y21p39BMc0qcFrq0sfafFUCbO0Ia7ORjYV1DqqkeGXM"
    try:
        send_notification(
            token=test_token,
            title="Test Notification",
            body="This is a test notification"
        )
    except Exception as e:
        print(f"Error: {str(e)}")