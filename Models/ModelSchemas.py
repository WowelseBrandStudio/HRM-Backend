import datetime
from mongoengine import connect, Document, StringField, EmailField, ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist,DateTimeField,DateField
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
    description = StringField(required=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_name = StringField(required=True)
    modified_at = DateTimeField(required=False)
    modified_by = StringField(required=False)
    modified_by_name = StringField(required=False)
    
class project_assigned_to(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    user_id = StringField(required=True)
    user_name = StringField(required=True)
    responsible = StringField(required=True)    
    created_at = DateTimeField(required=True,default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_name = StringField(required=True)
    modified_at = DateTimeField(required=True,default=datetime.datetime.now)
    modified_by = StringField(required=True)
    modified_by_name = StringField(required=True)

class timesheet(Document):
    objects = QuerySetManager()
    project_id = StringField(required=True)
    project_name = StringField(required=True)
    description = StringField(required=True)
    date = DateField(required=True)
    from_time = StringField(required=True)
    to_time = StringField(required=True)    
    created_at = DateTimeField(required=True,default=datetime.datetime.now)
    created_by = StringField(required=True)
    created_by_name = StringField(required=True)
    modified_at = DateTimeField(required=True,default=datetime.datetime.now)
    modified_by = StringField(required=True)
    modified_by_name = StringField(required=True)