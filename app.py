import datetime
from flask import Flask, jsonify, request
from mongoengine import connect, Document,DateField, StringField, EmailField, IntField,ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist,DateTimeField
from Controller.permission_controller import Permission
from Controller.project_assign_controller import Assign_projects
from Controller.project_controller import Projects
from Controller.timesheet_controller import Timesheets


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


@app.errorhandler(Exception)
def unknown_exception_err(error):
    return {"error": str(error)}, 500


def serialize_user(id):
    user_dict = id.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict


class Admin(Document):
    objects = QuerySetManager()
    password = StringField(required=True)
    name =StringField(required=True,unique=True)
    email = EmailField(required=True)
    mobile = StringField(required=False)


@app.route('/admin', methods=['GET','POST','DELETE'])
def admin():
    methods = {
        'POST': insert_admin,
        'GET': get_admin,
        'DELETE': delete_admin,
    }
    return methods.get(request.method)()
        

def insert_admin():
    data = request.form.to_dict()
    user = Admin(**data)
    user.save()
    return jsonify({"message":"Admin created successfully"})


def get_admin():
    admins = Admin.objects()    
    admins = [serialize_user(admin) for admin in admins]
 
    response_data = {
            "success": True,
            "data": admins,
            "msg": "Success" if admins else "Record not found"
        }
    
    return jsonify(response_data), 200

def update_admin():

    data =request.form.to_dict()
    admin = Admin.objects(id=data.get('id'))
    if not admin:
        return jsonify({"message":"Admin does not exists"}),404
    data.pop('_id')   
    admin.update(**data)
    return {"message": "Data updated successfully."},200

def delete_admin():
   
    data = request.get_json()
    admin = Admin.objects(id=data.get("id"))
    if not user:
        return jsonify({"message":"Admin not found"}), 404
    
    admin.delete()    
    return jsonify({"message":"Deleted successfully"}), 200
  
class User(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)
    role = StringField(required=True)
    name = StringField(required=True)
    dob = DateField(required=True)
    area = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField(required=False)
    # employee_id = StringField(required=True)
    report_to = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_name = StringField(required=True)
    modified_at = DateTimeField(required=False)
    modified_by = StringField(required=False)
    modified_by_name = StringField(required=False)    
    # permissions = ListField(StringField())
    # newpassword = StringField()
    # created_at = DateTimeField(default=datetime.now())
    
@app.route('/user', methods=['GET','POST','DELETE','PUT'])
def user():
    methods = {
        'POST': insert_user,
        'GET': get_user,
        'PUT':update_user,
        'DELETE':delete_user
    }
    return methods.get(request.method)()


def insert_user():
    data =request.form.to_dict()
    data['created_by'] = '1'
    data['created_by_name'] = 'test'
    user = User(**data)
    user.save()
    return jsonify({"message":"User created successfully"}),201



def get_user():
    users = User.objects()
    users = [serialize_user(user) for user in users]
  
    response_data = {
            "success": True,
            "data": users,
            "msg": "Success" if users else "Record not found"
        }
    
    return jsonify(response_data), 200

@app.route('/permission', methods=['GET', 'POST', 'DELETE', 'PUT'])
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


def update_user():

    data =request.form.to_dict()
    
    data['modified_at'] = datetime.datetime.now
    data['modified_by'] = '1'
    data['modified_by_name'] = 'test'
    
    user = User.objects(id=data.get('id'))
    if not user:
        return jsonify({"message":"user does not exists"}),404
    data.pop('id')   
    user.update(**data)
    return {"message": "Data updated successfully."},200

def delete_user():
   
    data = request.get_json()
    user = User.objects(id=data.get("id"))
    if not user:
        return jsonify({"message":"User not found"}), 404

    user.delete()    
    return jsonify({"message":"Deleted successfully"}), 200


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

if __name__ == '__main__':
    app.run(debug=True)

