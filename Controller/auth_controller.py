from flask import jsonify, request

from Models.ModelSchemas import Employee,Manager,Human_resource,Admin
from Utils.helper import JWTHandler


class Authentication:
    def __init__(self):
        pass

    def authenticate_user(self, role):
        possible_roles = ['Admin', 'User', 'HR', 'Manager']
        if role not in possible_roles:
            return jsonify({"mesage": "Invalid role"}), 400
        data = request.get_json()

        if role == 'Admin':
            collection_name = Admin
        elif role == 'User':
            collection_name = Employee
        elif role == 'Manager':
            collection_name = Manager
        else:
            collection_name = Human_resource

        username = data.get("username")
        password = data.get("password")
        user = collection_name.objects(email = username).first()
       
        if not user:
            return jsonify({"message":"Email does not exists"})
        
        # import pdb; pdb.set_trace()
        if  password != user["password"]:
            return jsonify({"mesage": "Password mismatch"}), 400
        
        payload = {
            "role": role,
            "username": username,
            "user_id":str(user['id'])
        }
       
        token = JWTHandler().generate_jwt(payload)
        return jsonify({"token": token}), 200
