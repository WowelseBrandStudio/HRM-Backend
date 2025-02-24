
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Project,Timesheet, Employee
from Utils.helper import create_response, roles_accepted, serialize_user


class Timesheets:
    def __init__(self):
        pass

    @roles_accepted('HR', 'User','Manager')
    def insert_timesheet(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()

        client_data = g.client_data
        user = Employee.objects(id=client_data['user_id']).first()

        data['user_id'] = client_data['user_id']
        data['user_name'] = user['name']
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

    
    @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_timesheet(self):

        timesheet = Timesheet.objects()

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

