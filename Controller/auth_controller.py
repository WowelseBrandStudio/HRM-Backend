from flask import jsonify, request

from Models.ModelSchemas import User
from Utils.helper import JWTHandler


class Authentication:
    def __init__(self):
        pass

    def authenticate_user(self, role):
        possible_roles = ['Admin', 'User', 'HR', 'Manager']
        if role not in possible_roles:
            return jsonify({"mesage": "Invalid role"}), 400
        data = request.get_json()
        
        username = data.get("username")
        password = data.get("password")
        user = User.objects(email = username).first()
               
        if not user:
            return jsonify({"message":"User does not exists"})
        
        # import pdb; pdb.set_trace()
        if  password != user["password"]:
            return jsonify({"mesage": "Password mismatch"}), 400
        
        payload = {
            "role": role,
            "username": username
        }
        token = JWTHandler().generate_jwt(payload)
        return jsonify({"token": token}), 200
