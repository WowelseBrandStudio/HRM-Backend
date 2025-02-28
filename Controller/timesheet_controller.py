
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import HOST, Admin, Human_resource, Manager, Project,Timesheet, Employee
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect


class Timesheets:
    def __init__(self):
        db_name = g.payload['app_id']
        
        disconnect('default')
        self.connect_to_db(db_name)
      

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )

    @roles_accepted('HR', 'User','Manager')
    def insert_timesheet(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()

        client_data = g.payload
        
        if client_data['role'] == 'HR':
            collection_name = Human_resource
        elif client_data['role'] == 'User':
            collection_name = Employee
        elif client_data['role'] == 'Manager':
            collection_name = Manager
    
        user = collection_name.objects(id=client_data['user_id']).first()

        data['user_id'] = client_data['user_id']
        data['user_name'] = user['first_name']
        data['project_name'] = project['project_name']
      
        
        timesheet = Timesheet(**data)
        timesheet.save()

        return create_response(True,"Timesheet created successfully",str(timesheet.id),None,200)

    
    @roles_accepted('HR', 'User','Manager')
    def update_timesheet(self):
  
        data = request.get_json()

        id = data.get("id")

        if data.get('project_id') != None:

            project_id = data.get('project_id')
            project = Project.objects(id=project_id).first()
            data['project_name'] = project['project_name']

        data['modified_at'] = datetime.datetime.now
    
        timesheet = Timesheet.objects(id=id).first()
        
        if not timesheet:
            return create_response(True,"Timesheet not found",None,None,404)

    
        data.pop('id')  
        timesheet.update(**data)
        return create_response(True,"Timesheet updated successfully",str(timesheet.id),None,200)

    
    # @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_timesheet(self):
        client_data = g.payload
        data = request.args.to_dict()
      
        
        if client_data['role'] == 'User':
            user_id =client_data['user_id']
        else:            
            user_id =  data.get('user_id') 
                
        user_filter={
            'user_id':user_id
        } if user_id else {}
        
        timesheet = Timesheet.objects(**user_filter)

        res_data = [serialize_user(record) for record in timesheet]
        return create_response(True,"Timesheet retrevied successfully",res_data,None,200)

    
    @roles_accepted('HR', 'User','Manager')
    def delete_timesheet(self):
    
        data = request.get_json()
        id = data.get("id")
        timesheet = Timesheet.objects(id=id).delete()

        if timesheet == 1:
            return create_response(True,"Timesheet Deleted successfully",None,None,200)

        else:
            return create_response(True,"Timesheet not found",None,None,404)

