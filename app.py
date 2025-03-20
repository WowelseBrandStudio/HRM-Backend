import datetime
from flask import Flask, g, jsonify, request
from flask_mail import Mail, Message
import jwt
from mongoengine import connect, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist
from Controller.admin_controller import Admins
from Controller.auth_controller import Authentication
from Controller.bonus_tip_controller import Bonus_tip
from Controller.dashboard_controller import Dashboard, UserInfo
from Controller.email_controller import init_mail
from Controller.hr_controller import  Human_resources
from Controller.manager_controller import Managers
from Controller.organisation_controller import Organization
from Controller.permission_controller import Permission
from Controller.user_controller import Employees
from Utils.helper import create_response, set_organisation, validate_token
from Controller.project_assign_controller import Assign_projects
from Controller.project_controller import Projects
from Controller.timesheet_controller import Timesheets

from mongoengine import disconnect
from flask_cors import CORS

#testS
app = Flask(__name__)
CORS(app)
# connect(
#     host = 'mongodb+srv://user:user@wowelse1.c179k.mongodb.net/?retryWrites=true&w=majority&appName=wowelse1',
#     db='company'
# )

# @app.after_request
# def after_request(response):
#     # Disconnect from the MongoDB default connection after the request
#     print("Disconnecting from the database")
#     disconnect('default')
#     return response

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'hrm25085@gmail.com'
app.config['MAIL_PASSWORD'] = 'bzbn azkg yeok cpia'
app.config['MAIL_DEFAULT_SENDER'] = 'hrm25085@gmail.com'
init_mail(app)


@app.errorhandler(NotUniqueError)
def handle_duplicate_error(error):
    return create_response(False,"data duplication error",None,str(error),400)

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return create_response(False,"validation error",None,str(error),400)

@app.errorhandler(DoesNotExist)
def handle_not_found_error(error):
    return create_response(False,"Data not found",None,str(error),400)
    

@app.errorhandler(jwt.ExpiredSignatureError)
def handle_signature_error(error):
    return create_response(False,"Token is expired",None,str(error),403)

@app.errorhandler(jwt.InvalidTokenError)
def  handle_invalid_token_error(error):
  
    return create_response(False,"Invalid token",None,str(error),401)

@app.errorhandler(Exception)
def unknown_exception_err(error):    
    return create_response(False,"Exceptional",None,str(error),401)



def serialize_user(id):
    user_dict = id.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict

# @app.before_request
# def before_request():
#     headers = request.headers
#     api_key = headers.get("x-api-key")
#     api_key_secret = headers.get("x-api-secrect")
#     if api_key is None or api_key_secret is None:
#         return jsonify({"error": "Headers missing"}), 401
    

@app.route('/organisation', methods=['GET', 'POST'])
def organisation():
    """
    1. Handle all operations related to organisation
    2. GET - Fetch details of organisation
    3. POST - Create new organisation
    """
    obj = Organization()
    methods = {
        'GET': obj.get_organization_by_id,
        'POST': obj.insert_organization,
        'PUT': "update_organisation",
    }
    return methods.get(request.method)()



@app.route('/permission', methods=['GET', 'POST', 'DELETE', 'PUT'])
@validate_token
def permission():
    """
    1. Handle all those permissions 
    2. insert - User those who requested permission
    3. GET - Fetch all permission requests who is responsible
    4. DELETE - Optional 
    """
    # app_id = g.app_id
    obj = Permission()
    methods = {
        'GET': obj.get_permission_requested_list,
        'POST': obj.request_permission,
        'PUT': obj.update_permission,
        'DELETE': obj.delete_permission,
    }
    return methods.get(request.method)()


@app.route('/login', methods=['POST'])
@set_organisation
def login():
    obj = Authentication(g.app_id)
    role = request.args.get("role")
    return obj.authenticate_user(role)

@app.route('/project', methods=['GET', 'POST', 'DELETE', 'PUT'])
@validate_token
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
@validate_token
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
@validate_token
def timesheet():
    
    obj = Timesheets()
    methods = {
        'GET': obj.get_all_timesheet,
        'POST': obj.insert_timesheet,
        'PUT': obj.update_timesheet,
        'DELETE': obj.delete_timesheet,
    }
    return methods.get(request.method)()

@app.route('/employee', methods=['GET', 'POST', 'DELETE', 'PUT'])
@validate_token
def employee():
    
    obj = Employees()
    methods = {
        'GET': obj.get_all_employee,
        'POST': obj.insert_employee,
        'PUT': obj.update_employee,
        'DELETE': obj.delete_employee,
    }
    return methods.get(request.method)()


@app.route('/admin', methods=['GET', 'POST', 'DELETE', 'PUT'])
@validate_token
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
@validate_token
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
@validate_token
def manager():
    
    obj = Managers()
    methods = {
        'GET': obj.get_all_manager,
        'POST': obj.insert_manager,
        'PUT': obj.update_manager,
        'DELETE': obj.delete_manager,
    }
    return methods.get(request.method)()


@app.route('/bonus_tip', methods=['GET', 'POST', 'DELETE', 'PUT'])
@validate_token
def bonus_tip():
    
    obj = Bonus_tip()
    methods = {
        'GET': obj.get_all_bonus,
        'POST': obj.insert_bonus,
        'PUT': obj.update_bonus,
        'DELETE': obj.delete_bonus,
    }
    return methods.get(request.method)()


@app.route('/user_info', methods=['GET'])
@validate_token
def user_info():
    
    obj = UserInfo()
    methods = {
        'GET': obj.user_info,        
    }
    return methods.get(request.method)()


@app.route('/dashboard_count', methods=['GET'])
@validate_token
def dashboard_count():
    obj = Dashboard()
    methods = {
        'GET': obj.dashboard_count,        
    }
    return methods.get(request.method)()

if __name__ == '__main__':
    app.run(debug=True)

