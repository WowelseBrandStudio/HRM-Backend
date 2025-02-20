import datetime
from functools import wraps

from flask import g, jsonify, request
import jwt


def serialize_user(user):
    user_dict = user.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict


def roles_accepted(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return jsonify({"error": "Missing Authorization header"}), 401
            token = request.headers.get('Authorization').split()[1]
            decode_data = JWTHandler().decode_jwt(token)
            if not decode_data:
                return jsonify({"error": "Invalid token"}), 403
            user_role = decode_data['role']  #NOTE: Get the role from token
            g.client_data = decode_data 
            if user_role not in roles:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

class JWTHandler:
    def __init__(self, key = "qwertyuiopasdfghjkzxcvbnm"):
        self.SECRET_KEY = key


    def generate_jwt(self, payload: dict) -> str:
        expiration_time = datetime.datetime.now(
        ) + datetime.timedelta(minutes=120)  # Token expires in 1 hour
        payload['exp'] = expiration_time.timestamp()
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token


    def decode_jwt(self, token: str) -> dict:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        return payload
        # try:
        # except jwt.ExpiredSignatureError:
        #     return {"error": "Token expired"}
        # except jwt.InvalidTokenError:
        #     return {"error": "Invalid token"}
