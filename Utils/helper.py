import datetime
from functools import wraps

from flask import g, jsonify, request
import jwt

from Models.ModelSchemas import organization


def serialize_user(user):
    user_dict = user.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict

def set_organisation(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'x-api-key' not in request.headers:
            return jsonify({"error": "Missing x-api-key header"}), 400
        if 'x-api-secret' not in request.headers:
            return jsonify({"error": "Missing x-api-secret header"}), 400
        api_key = request.headers.get('x-api-key')
        api_secret = request.headers.get('x-api-secret')
        # connect_to_db('organisation_handler')
        org = organization.objects(api_key=api_key, api_secret=api_secret).first()
        if not org:
            return jsonify({"error": "Invalid API key or secret"}), 403
        g.app_id = org.app_id
        return f(*args, **kwargs)
    return wrapper

def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({"error": "Missing Authorization header"}), 401
        token = request.headers.get('Authorization').split()[1]
        decode_data = JWTHandler().decode_jwt(token)
        if not decode_data:
            return jsonify({"error": "Invalid token"}), 403
        g.payload = decode_data
        return f(*args, **kwargs)
    return wrapper

    # return g.app_id if hasattr(g, 'app_id') else None


def roles_accepted(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # if 'Authorization' not in request.headers:
            #     return jsonify({"error": "Missing Authorization header"}), 401
            # token = request.headers.get('Authorization').split()[1]
            # decode_data = JWTHandler().decode_jwt(token)
            # if not decode_data:
            #     return jsonify({"error": "Invalid token"}), 403
            # user_role = decode_data['role']  #NOTE: Get the role from token
            # g.client_data = decode_data 
            # g.payload = jsonify(decode_data)
            if g.payload['role'] not in roles:
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

def create_response(success: bool, message: str, data=None, error=None, status_code=200):
    """
    Create a consistent response structure for success and failure.
    """
    response = {
        "success": success,   # True | False
        "message": message,   # Client-side message
        "data": data if data else {}, # Client-side data
        "error": error if error else None # Client-side error
    }
    return jsonify(response), status_code
