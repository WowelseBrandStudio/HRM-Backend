from flask import jsonify, request

from Models.ModelSchemas import HOST, Employee,Manager,Human_resource,Admin
from Utils.helper import JWTHandler, create_response
from mongoengine import connect, disconnect


class Authentication:
    def __init__(self,app_id):
        self.app_id = app_id
        # disconnect('organisation_handler')
        disconnect('default')
        self.connect_to_db(self.app_id)

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )
        print(f"Connecting to the database: {self.app_id}")

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
            # return jsonify({"mesage": "Password mismatch"}), 400
            return create_response(False,"password mmismatch",None,"password mismatch",400)
        
        payload = {
            "role": role,
            "username": username,
            "user_id":str(user['id']),
            "app_id":self.app_id
        }
       
        token = JWTHandler().generate_jwt(payload)
        # return jsonify({"token": token}), 200
        return create_response(True,"login success",token,None,200)
