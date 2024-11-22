import http.client
import json

class OTPService:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("v31v9r.api.infobip.com")
        self.headers = {
            'Authorization': 'App e2067ecb3ab2d3c784d3f7686d6aa6bd-53d80cf4-b913-4dd0-83ac-44d893cc7d22',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def send_otp(self, phone_number: str, otp: str) -> bool:
        payload = json.dumps({
            "messages": [
                {
                    "destinations": [{"to": phone_number}],
                    "from": "ServiceSMS",
                    "text": f"Your OTP is: {otp}. Please use this to verify your account."
                }
            ]
        })

        self.conn.request("POST", "/sms/2/text/advanced", payload, self.headers)
        res = self.conn.getresponse()

        if res.status == 200:
            data = res.read()
            response = json.loads(data.decode("utf-8"))
            print(f"OTP sent successfully {response}")
            return True
        return False