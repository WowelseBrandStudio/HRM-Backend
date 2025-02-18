
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Project, Assign_project,User
from Utils.helper import serialize_user


class Assign_projects:
    def __init__(self):
        pass

    
    def insert_assign_project(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()

        user_id = data.get('user_id')
        user = User.objects(id=user_id).first()

        data['created_by'] = '1'
        data['created_by_name'] = 'test'
        data['project_name'] = project['project_name']
        data['user_name'] = user['name']
        
        assign_project = Assign_project(**data)
        assign_project.save()

        return jsonify({"message":"Project assigned successfully"}),201
    
    def update_assign_project(self):
  
        data = request.get_json()

        id = data.get("id")

        if data.get('project_id') != None:

            project_id = data.get('project_id')
            project = Project.objects(id=project_id).first()
            data['project_name'] = project['project_name']


        if data.get('user_id') != None:

            user_id = data.get('user_id')
            user = User.objects(id=user_id).first()
            data['user_name'] = user['name']

        data['modified_at'] = datetime.datetime.now
        data['modified_by'] = '1'
        data['modified_by_name'] = 'test'

        assign_project = Assign_project.objects(id=id).first()
        
        if not assign_project:
            return jsonify({"message":"Project assign not found"}),404
    
        data.pop('id')  
        assign_project.update(**data)
        return jsonify({"message": "Assign Project updated successfully"}),200
    
        
    def get_all_assigned_project(self):

        assign_project = Assign_project.objects()

        res_data = [serialize_user(record) for record in assign_project]
        return jsonify({"message": "Assign Project retrevied successfully", "data": res_data}),200
    
        
    def delete_assign_project(self):
    
        data = request.get_json()
        id = data.get("id")
        assign_project = Assign_project.objects(id=id).first()

        if not assign_project:
            return jsonify({"message":"Assign Project not found"}), 404
        
        assign_project.delete()    
        return jsonify({"message":"Assigned project Deleted successfully"}), 200