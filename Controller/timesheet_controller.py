
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import HOST, Admin, Human_resource, Manager, Project,Timesheet, Employee
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist


class Timesheets:
    def __init__(self):
        pass
        # db_name = g.payload['app_id']
        
        # # disconnect('default')
        # self.connect_to_db(db_name)
      

    def connect_to_db(self, db_name,alias='default'):
        # Dynamically switch the database based on app_id
        # connect(
        #     host = HOST,
        #     db = db_name,
        # )
        disconnect(alias)  # Disconnect previous connection
        return connect(db=db_name, host=HOST, alias=alias)

    @roles_accepted('HR', 'User','Manager')
    def insert_timesheet(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()
        if not project:
            raise DoesNotExist('Project not found') 
       
        client_data = g.payload
   
        if client_data['role'] == 'HR':
            collection_name = Human_resource
        elif client_data['role'] == 'User':
            collection_name = Employee
        elif client_data['role'] == 'Manager':
            collection_name = Manager
    
        user = collection_name.objects(id=client_data['user_id']).first()
        if not user:
            raise DoesNotExist('User not found') 

        data['user_id'] = client_data['user_id']
        data['user_name'] = user['first_name']
        data['responsible_hr'] = user['responsible_hr']
        data['responsible_manager'] = user['responsible_manager']
        data['project_name'] = project['project_name']
      
        
        timesheet = Timesheet(**data)
        timesheet.save()

        return create_response(True,"Timesheet created successfully",str(timesheet.id),None,200)

    
    @roles_accepted('HR', 'User','Manager')
    def update_timesheet(self):
  
        data = request.get_json()

        id = data.get("id")

        data['modified_at'] = datetime.datetime.now
    
        timesheet = Timesheet.objects(id=id).first()
        
        if not timesheet:
            raise DoesNotExist(f'Timesheet {id} not found') 
    
        data.pop('id')  
        timesheet.update(**data)
        return create_response(True,"Timesheet updated successfully",str(timesheet.id),None,200)

    
    # @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_timesheet(self):
        client_data = g.payload  
        filter = request.args.to_dict()      
        
        roles = {
            'Manager': lambda: filter.update({"responsible_manager": client_data['user_id']}),
            'HR': lambda: filter.update({"responsible_hr": client_data['user_id']}),
            'User': lambda: filter.update({"user_id": client_data['user_id']})
            
        }
       
        roles.get(client_data['role'], lambda: None)()
        timesheet = Timesheet.objects(**filter)

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

