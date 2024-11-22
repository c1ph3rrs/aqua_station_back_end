import http.client
import json

class OTPService:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("69ngp5.api.infobip.com")
        self.headers = {
            'Authorization': 'App 982e4fc3b4209f71c028e10c274bf34d-3f401dc0-ec17-4eb2-8022-210b141fcd25',
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
            # print(f"OTP sent successfully {response}")
            return True
        return False