import requests

class OTPService:
    def __init__(self) -> None:
        self.api_user = "xfe9q3yv"
        self.api_password = "dk3PbcOU"
        self.sender_id = "AquaStation"

    def send_otp(self, recipient_number: str, otp_code: str) -> bool:
        message = f"Your OTP code is {otp_code}"
        response = self.send_sms(self.api_user, self.api_password, self.sender_id, recipient_number, message)
        return response.status_code in [200, 202]

    def send_sms(self, api_user: str, api_password: str, sender_id: str, recipient_number: str, message: str) -> requests.Response:
        url = "https://api.smsglobal.com/http-api.php"
        payload = f'action=sendsms&user={api_user}&password={api_password}&from={sender_id}&to={recipient_number}&text={message}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload)
        return response