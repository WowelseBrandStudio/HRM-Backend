import datetime
from mongoengine import connect, disconnect, Document, StringField, EmailField, ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist,DateTimeField,DateField,IntField
import configparser

# Read the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Establish connection to MongoDB
HOST = config.get('DEFAULT',"HOST")

# def connect_to_db(db_name):
#     """
#     Connect to the database only when needed.
#     """
#     print(f"Connecting to MongoDB - {db_name}")
    
#     # Disconnect from the previous connection (if any)
#     # disconnect('default')  # This disconnects the current 'default' connection
    
#     # Connect to the new database with a custom alias
#     # connect(db_name, host=HOST, alias=db_name)
#     connect(host=HOST, db=db_name, alias=db_name)

# connect(
#     host = HOST,
#     # db='company',
#     db='organisation_handler',
# )
class organization(Document):
    objects = QuerySetManager()
    org_name = StringField(required=True)
    org_type = StringField(required=True)
    org_description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    api_key = StringField(required=True)
    api_secret = StringField(required=True)
    app_id = StringField(required=True)

class permission_request(Document):
    objects = QuerySetManager()
    leave_type = StringField(required=True, default = 'cl', choices = ['cl', 'sick', 'permission'])
    reason = StringField(required=True)
    reporting_to = StringField(required=True)
    approval_sts = StringField(choices = ['approved', 'declined', 'pending'])
    from_date = StringField(required=True)
    to_date = StringField(required=True)
    from_time = StringField()
    to_time = StringField()
    title = StringField()
    reject_description = StringField()
    user_id = StringField()

class Project(Document):
    objects = QuerySetManager()
    project_name = StringField(required=True)
    department = StringField(required=True,choices = ['Development','Digital_marketing'])
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()
    
class Assign_project(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    responsible = StringField(required=True)    
    assigned_at = DateTimeField(default=datetime.datetime.now)
    assigned_by = StringField(required=True)   
    assigned_by_role = StringField(required=True)   
    modified_at = DateTimeField()
      

class Timesheet(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    description = StringField(required=True)
    title = StringField(required=True)
    date = DateField(required=True)
    from_time = StringField(required=True)
    to_time = StringField(required=True)    
    created_at = DateTimeField(default=datetime.datetime.now)
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    modified_at = DateTimeField()


class Employee(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    dob = StringField(required=True)
    age = StringField(required=True)
    date_of_join = StringField(required=True)
    address_1 = StringField(required=True)
    address_2 = StringField(required=True)
    area = StringField(required=True)
    experience = IntField(required=True)
    position = StringField(required=True)
    district = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField(choices = ['Male','Female','Others'])
    user_id = StringField(required=True)
    responsible_hr = StringField(required=True)
    responsible_manager = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()

class Human_resource(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    dob = StringField(required=True)
    age = StringField(required=True)
    date_of_join = StringField(required=True)
    address_1 = StringField(required=True)
    address_2 = StringField(required=True)
    area = StringField(required=True)
    position = StringField(required=True)
    experience = IntField(required=True)
    district = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField(choices = ['Male','Female','Others'])
    user_id = StringField(required=True)   
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_role = StringField(required=True)
    modified_at = DateTimeField()

class Manager(Document):
    objects = QuerySetManager()   
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)   
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    dob = StringField(required=True)
    age = StringField(required=True)
    date_of_join = StringField(required=True)
    address_1 = StringField(required=True)
    address_2 = StringField(required=True)
    area = StringField(required=True)
    experience = IntField(required=True)
    position = StringField(required=True)
    district = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField(choices = ['Male','Female','Others'])
    user_id = StringField(required=True)   
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
    user_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)


class Bonus(Document):
    objects = QuerySetManager()
    user_id = StringField(required=True)
    bonus_given_by =StringField(required=True)
    tip_code = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField()