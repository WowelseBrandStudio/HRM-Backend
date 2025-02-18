from flask import Flask, jsonify, request
import jwt
from mongoengine import connect, Document, StringField, EmailField, ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist
from Controller.auth_controller import Authentication
from Controller.permission_controller import Permission
from Utils.helper import roles_accepted

#testS
app = Flask(__name__)

connect(
    host = 'mongodb+srv://user:user@wowelse1.c179k.mongodb.net/?retryWrites=true&w=majority&appName=wowelse1',
    db='company'
)

@app.errorhandler(NotUniqueError)
def handle_duplicate_error(error):
    return {"error": str(error)}, 400

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return {"error": str(error)}, 400

@app.errorhandler(DoesNotExist)
def handle_not_found_error(error):
    return {"error": str(error)}, 404

@app.errorhandler(jwt.ExpiredSignatureError)
def handle_signature_error(error):
    return jsonify({"error": "Token is expired"}), 403

@app.errorhandler(jwt.InvalidTokenError)
def  handle_invalid_token_error(error):
    return jsonify({"error": "Invalid token"}), 401

@app.errorhandler(Exception)
def unknown_exception_err(error):
    return {"error": str(error)}, 500

class Admin(Document):
    objects = QuerySetManager()
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

@app.route('/user', methods=['GET','POST'])
def user():
    methods = {
        'POST': insert,
        'GET': get
    }
    return methods.get(request.method)()

class User(Document):
    objects = QuerySetManager()
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    role = StringField(required=True)
    permissions = ListField(StringField())
    newpassword = StringField()
    # created_at = DateTimeField(default=datetime.now())

@app.route('/admin', methods=['GET','POST'])
def admin():
    methods = {
        'POST': "insert_admin",
        'GET': "get_admin"
    }
    return methods.get(request.method)()
        

def insert():
    data = request.get_json()
    user = User(**data)
    user.save()
    return 'User created successfully'

def serialize_user(user):
    user_dict = user.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict

def get():
    users = User.objects()
    # users = [user.to_json() for user in users]
    # users = [user.to_mongo().to_dict() for user in users]
    users = [serialize_user(user) for user in users]
    response_data = {
            "success": True,
            "data": users,
            "msg": "Success" if users else "Record not found"
        }
    return jsonify(response_data), 200

@app.route('/permission', methods=['GET', 'POST', 'DELETE', 'PUT'])
@roles_accepted('Admin', 'User', 'HR', 'Manager')
def permission():
    """
    1. Handle all those permissions 
    2. insert - User those who requested permission
    3. GET - Fetch all permission requests who is responsible
    4. DELETE - Optional 
    """
    obj = Permission()
    methods = {
        'GET': obj.get_permission_requested_list,
        'POST': obj.request_permission,
        'PUT': obj.update_permission,
        'DELETE': obj.delete_permission,
    }
    return methods.get(request.method)()

@app.route('/login', methods=['POST'])
def login():
    obj = Authentication()
    role = request.args.get("role")
    return obj.authenticate_user(role)


if __name__ == '__main__':
    app.run(debug=True)



# DEPRECATED:
# res = serialize_single_user(users)
# "data": [serialize_user(user) for user in users]



# def serialize_single_user(user):
#     return {
#         "_id": str(user.id),  # Convert ObjectId to string
#         "username": user.username,
#         "email": user.email,
#         "role": user.role,
#         "permissions": user.permissions
#     } if user else None