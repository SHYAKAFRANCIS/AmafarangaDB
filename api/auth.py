import base64

USERNAME = "admin"
PASSWORD = "password"

def check_auth(headers):
        """ checks for valide authentication"""
        auth_header = headers.get("Authorization")
        if not auth_header:
            return False
        try:
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = self.base64.b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":")
            return username == self.USERNAME and password == self.PASSWORD
        except Exception:
            return False