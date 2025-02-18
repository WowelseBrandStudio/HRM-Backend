import datetime
from flask import Flask, jsonify, request
import jwt
from mongoengine import connect, Document,DateField, StringField, EmailField, IntField,ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist,DateTimeField
from Controller.admin_controller import Admins
from Controller.auth_controller import Authentication
from Controller.hr_controller import  Human_resources
from Controller.manager_controller import Managers
from Controller.permission_controller import Permission
from Controller.user_controller import Users
from Models.ModelSchemas import Manager
from Utils.helper import roles_accepted
from Controller.project_assign_controller import Assign_projects
from Controller.project_controller import Projects
from Controller.timesheet_controller import Timesheets

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


def serialize_user(id):
    user_dict = id.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict

@app.route('/permission', methods=['GET', 'POST', 'DELETE', 'PUT'])
@roles_accepted('Admin', 'HR', 'Manager')
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

@app.route('/project', methods=['GET', 'POST', 'DELETE', 'PUT'])
def project():
    
    obj = Projects()
    methods = {
        'GET': obj.get_all_project,
        'POST': obj.insert_project,
        'PUT': obj.update_project,
        'DELETE': obj.delete_project,
    }
    return methods.get(request.method)()


@app.route('/assign_project', methods=['GET', 'POST', 'DELETE', 'PUT'])
def assign_project():
    
    obj = Assign_projects()
    methods = {
        'GET': obj.get_all_assigned_project,
        'POST': obj.insert_assign_project,
        'PUT': obj.update_assign_project,
        'DELETE': obj.delete_assign_project,
    }
    return methods.get(request.method)()


@app.route('/timesheet', methods=['GET', 'POST', 'DELETE', 'PUT'])
def timesheet():
    
    obj = Timesheets()
    methods = {
        'GET': obj.get_all_timesheet,
        'POST': obj.insert_timesheet,
        'PUT': obj.update_timesheet,
        'DELETE': obj.delete_timesheet,
    }
    return methods.get(request.method)()

@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user():
    
    obj = Users()
    methods = {
        'GET': obj.get_all_user,
        'POST': obj.insert_user,
        'PUT': obj.update_user,
        'DELETE': obj.delete_user,
    }
    return methods.get(request.method)()


@app.route('/admin', methods=['GET', 'POST', 'DELETE', 'PUT'])
def admin():
    
    obj = Admins()
    methods = {
        'GET': obj.get_all_admin,
        'POST': obj.insert_admin,
        'PUT': obj.update_admin,
        'DELETE': obj.delete_admin,
    }
    return methods.get(request.method)()


@app.route('/hr', methods=['GET', 'POST', 'DELETE', 'PUT'])
def human_resource():
    
    obj = Human_resources()
    methods = {
        'GET': obj.get_all_hr,
        'POST': obj.insert_hr,
        'PUT': obj.update_hr,
        'DELETE': obj.delete_hr,
    }
    return methods.get(request.method)()


@app.route('/manager', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manager():
    
    obj = Managers()
    methods = {
        'GET': obj.get_all_manager,
        'POST': obj.insert_manager,
        'PUT': obj.update_manager,
        'DELETE': obj.delete_manager,
    }
    return methods.get(request.method)()

if __name__ == '__main__':
    app.run(debug=True)

