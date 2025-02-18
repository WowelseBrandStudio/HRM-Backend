import datetime
from mongoengine import connect, Document, StringField, EmailField, ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist,DateTimeField,DateField,IntField
import configparser

# Read the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Establish connection to MongoDB
HOST = config.get('DEFAULT',"HOST")

connect(
    host = HOST,
    db='company'
)

class permission_request(Document):
    objects = QuerySetManager()
    leave_type = StringField(required=True, default = 'cl', choices = ['cl', 'sick', 'permission'])
    reason = StringField(required=True)
    reporting_to = StringField(required=True)
    approval_sts = StringField(required=True)
    from_date = StringField(required=True)
    to_date = StringField(required=True)


class Project(Document):
    objects = QuerySetManager()
    project_name = StringField(required=True)
    department = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_name = StringField(required=True)
    modified_at = DateTimeField()
    modified_by = StringField()

    
class Assign_project(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    responsible = StringField(required=True)    
    assigned_at = DateTimeField(default=datetime.datetime.now)
    assigned_by = StringField(required=True)   
    modified_at = DateTimeField()
    modified_by = StringField()
   

class Timesheet(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    description = StringField(required=True)
    date = DateField(required=True)
    from_time = StringField(required=True)
    to_time = StringField(required=True)    
    created_at = DateTimeField(default=datetime.datetime.now)
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    modified_at = DateTimeField()


class User(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    name = StringField(required=True)
    dob = StringField(required=True)
    area = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField()
    # employee_id = StringField(required=True)
    reporting_hr = StringField(required=True)
    reporting_manager = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()


class Human_resource(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    name = StringField(required=True)
    dob = StringField(required=True)
    area = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField()
    # employee_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()


class Manager(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    name = StringField(required=True)
    dob = StringField(required=True)
    area = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField()
    # employee_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()

class Admin(Document):
    objects = QuerySetManager()
    password = StringField(required=True)
    name =StringField(required=True)
    email = EmailField(required=True,unique=True)
    mobile = StringField(required=True,unique=True)