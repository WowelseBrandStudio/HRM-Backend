from mongoengine import connect, Document, StringField, EmailField, ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist
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
