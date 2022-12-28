
import base64
import datetime
import hashlib
import secrets


class WSSEAuthenticator:
    def __init__(self, hatena_id: str, api_key: str) -> None:
        self.hatena_id = hatena_id
        self.api_key = api_key

    def generateheader(self) -> tuple[str, str]:
        nonce = secrets.token_hex(16)
        created = datetime.datetime.now().isoformat()
        password_digest = base64.b64encode(hashlib.sha1(
            (nonce+created+self.api_key).encode()).digest()).decode()
        return ("X-WSSE", f'UsernameToken Username="{self.hatena_id}", PasswordDigest="{password_digest}", Nonce="{nonce}", Created="{created}"')


class BasicAuthenticator:
    def __init__(self, hatena_id: str, api_key: str) -> None:
        self.hatena_id = hatena_id
        self.api_key = api_key

    def generateheader(self) -> tuple[str, str]:
        credential = base64.b64encode(
            (self.hatena_id + ":" + self.api_key).encode()).decode()
        return ("Authorization", f'Basic {credential}')
