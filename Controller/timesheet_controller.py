
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Project,Timesheet, Employee
from Utils.helper import roles_accepted, serialize_user


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

        return jsonify({"message":"Timesheet created successfully"}),201
    
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
            return jsonify({"message":"Timesheet not found"}),404
    
        data.pop('id')  
        timesheet.update(**data)
        return jsonify({"message": "Timesheet updated successfully"}),200
    
    @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_timesheet(self):

        timesheet = Timesheet.objects()

        res_data = [serialize_user(record) for record in timesheet]
        return jsonify({"message": "Timesheet retrevied successfully", "data": res_data}),200
    
    @roles_accepted('HR', 'User','Manager')
    def delete_timesheet(self):
    
        data = request.get_json()
        id = data.get("id")
        timesheet = Timesheet.objects(id=id).delete()

        if timesheet == 1:
            return jsonify({"message":"Timesheet Deleted successfully"}), 200
        else:
            return jsonify({"message":"Timesheet not found"}), 404