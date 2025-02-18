
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Project
from Utils.helper import serialize_user


class Projects:
    def __init__(self):
        pass

    
    def insert_project(self):

        data = request.get_json()       
        data['created_by'] = '1'
        data['created_by_name'] = 'test'

        project = Project(**data)
        project.save()
        return jsonify({"message":"Project created successfully"})
    
    def update_project(self):
  
        data = request.get_json()

        id = data.get("id")
        data['modified_at'] = datetime.datetime.now
        data['modified_by'] = '1'
        data['modified_by_name'] = 'test'

        project = Project.objects(id=id)
        if not project:
            return jsonify({"message":"Project not found"}), 
    
        data.pop('id')  
        project.update(**data)
        return jsonify({"message": "Project updated successfully"})
    
        
    def get_all_project(self):

        project = Project.objects()
        res_data = [serialize_user(record) for record in project]
        return jsonify({"message": "Project retrevied successfully", "data": res_data})
    
        
    def delete_project(self):
    
        data = request.get_json()
        project = Project.objects(id=data.get("id"))
        if not project:
            return jsonify({"message":"Project not found"}), 404
        
        project.delete()    
        return jsonify({"message":"Project Deleted successfully"}), 200