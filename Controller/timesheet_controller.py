
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Project,Timesheet
from Utils.helper import serialize_user


class Timesheets:
    def __init__(self):
        pass

    
    def insert_timesheet(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()

        data['created_by'] = '1'
        data['created_by_name'] = 'test'
        data['project_name'] = project['project_name']
      
        
        timesheet = Timesheet(**data)
        timesheet.save()

        return jsonify({"message":"Timesheet created successfully"}),201
    
    def update_timesheet(self):
  
        data = request.get_json()

        id = data.get("id")

        if data.get('project_id') != None:

            project_id = data.get('project_id')
            project = Project.objects(id=project_id).first()
            data['project_name'] = project['project_name']

        data['modified_at'] = datetime.datetime.now
        data['modified_by'] = '1'
        data['modified_by_name'] = 'test'

        timesheet = Timesheet.objects(id=id).first()
        
        if not timesheet:
            return jsonify({"message":"Timesheet not found"}),404
    
        data.pop('id')  
        timesheet.update(**data)
        return jsonify({"message": "Timesheet updated successfully"}),200
    
        
    def get_all_timesheet(self):

        timesheet = Timesheet.objects()

        res_data = [serialize_user(record) for record in timesheet]
        return jsonify({"message": "Timesheet retrevied successfully", "data": res_data}),200
    
        
    def delete_timesheet(self):
    
        data = request.get_json()
        id = data.get("id")
        timesheet = Timesheet.objects(id=id).first()

        if not timesheet:
            return jsonify({"message":"Timesheet not found"}), 404
        
        timesheet.delete()    
        return jsonify({"message":"Timesheet Deleted successfully"}), 200