import jwt
import datetime

from utils.utils import get_server_secret_key


def encode_user_token(user_address: str):
    try:
        sec_key = get_server_secret_key()
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "sub": user_address,
        }
        return jwt.encode(payload, sec_key, algorithm="HS256")
    except Exception as e:
        print("EXCEPTION IN ENCODING JWT TOKEN", e)
        raise e
