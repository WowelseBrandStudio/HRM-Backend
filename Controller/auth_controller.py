from flask import jsonify, request

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
        server_side_data = {
            "username": "admin",
            "password": "admin"
        }
        # import pdb; pdb.set_trace()
        if username != server_side_data["username"] or password != server_side_data["password"]:
            return jsonify({"mesage": "Invalid credentials"}), 400
        payload = {
            "role": role,
            "username": username
        }
        token = JWTHandler().generate_jwt(payload)
        return jsonify({"token": token}), 200
