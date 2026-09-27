import jwt
import json
from datetime import timedelta, datetime

secret = "fjbhvg5v4g5v45gv45nmnbmgnbbv6b5v56c565cv65nmbnbnkgjkkj4k5j465"

def jwt_encode(user_id):
    sub = json.dumps({"user_id": user_id})

    payload = {
        "sub": sub,
        "exp": datetime.now() + timedelta(days=10)
    }

    return jwt.encode(payload=payload, key=secret, algorithm="HS256")


def jwt_verify(jwt_token):
    try:
        user_id = json.loads(jwt.decode(jwt_token, key=secret, algorithms=["HS256"])["sub"])["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        raise "JWT token was expired"