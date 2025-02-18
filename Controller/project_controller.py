
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Project
from Utils.helper import serialize_user


class Projects:
    def __init__(self):
        pass

    
    def insert_project(self):

        data = request.get_json()       
        possible_dep =['Development','Digital_marketing']
        if data.get('department') not in possible_dep:
            return jsonify({"message":"invalid department","avaialble_dep":possible_dep})
        data['created_by'] = '1'
        data['created_by_name'] = 'test'

        project = Project(**data)
        project.save()
        return jsonify({"message":"Project created successfully"}),201
    
    def update_project(self):
  
        data = request.get_json()

        id = data.get("id")
        possible_dep =['Development','Digital_marketing']
        
        if data.get('department') !=  None:
            if data.get('department') not in possible_dep:
                return jsonify({"message":"invalid department","avaialble_dep":possible_dep})
        
        data['modified_at'] = datetime.datetime.now
        data['modified_by'] = '1'
        

        project = Project.objects(id=id).first()
        if not project:
            return jsonify({"message":"Project not found"}), 404
    
        data.pop('id')  
        project.update(**data)
        return jsonify({"message": "Project updated successfully"}),200
    
        
    def get_all_project(self):

        project = Project.objects()
        res_data = [serialize_user(record) for record in project]
        return jsonify({"message": "Project retrevied successfully", "data": res_data}),200
    
        
    def delete_project(self):
    
        data = request.get_json()
        id = data.get("id")
        project = Project.objects(id=id).first()
        if not project:
            return jsonify({"message":"Project not found"}), 404
        
        project.delete()    
        return jsonify({"message":"Project Deleted successfully"}), 200