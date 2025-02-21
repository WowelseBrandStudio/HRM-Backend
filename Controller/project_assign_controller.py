
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Project, Assign_project,Employee
from Utils.helper import roles_accepted, serialize_user


class Assign_projects:
    def __init__(self):
        pass

    @roles_accepted('Admin', 'HR','Manager')    
    def insert_assign_project(self):

        data = request.get_json()  

        project_id = data.get('project_id')
        project = Project.objects(id=project_id).first()

        user_id = data.get('user_id')
        user = Employee.objects(id=user_id).first()
        client_data = g.client_data
        data['assigned_by'] = client_data['user_id']
        data['assigned_by_role'] = client_data['role']
        data['project_name'] = project['project_name']
        data['user_name'] = user['name']
        
        assign_project = Assign_project(**data)
        assign_project.save()

        return jsonify({"message":"Project assigned successfully"}),201
    
    @roles_accepted('Admin', 'HR','Manager')
    def update_assign_project(self):
  
        data = request.get_json()

        id = data.get("id")

        if data.get('project_id') != None:

            project_id = data.get('project_id')
            project = Project.objects(id=project_id).first()
            data['project_name'] = project['project_name']


        if data.get('user_id') != None:

            user_id = data.get('user_id')
            user = Employee.objects(id=user_id).first()
            data['user_name'] = user['name']

        data['modified_at'] = datetime.datetime.now
      
        assign_project = Assign_project.objects(id=id).first()
        
        if not assign_project:
            return jsonify({"message":"Project assign not found"}),404
    
        data.pop('id')  
        assign_project.update(**data)
        return jsonify({"message": "Assign Project updated successfully"}),200
    
    @roles_accepted('Admin', 'HR', 'User','Manager')        
    def get_all_assigned_project(self):

        assign_project = Assign_project.objects()

        res_data = [serialize_user(record) for record in assign_project]
        return jsonify({"message": "Assign Project retrevied successfully", "data": res_data}),200
    
    @roles_accepted('Admin', 'HR','Manager')    
    def delete_assign_project(self):
    
        data = request.get_json()
        id = data.get("id")
        assign_project = Assign_project.objects(id=id).delete()
        if assign_project == 1:
            return jsonify({"message":"Assign project Deleted successfully"}), 200
        else:
            return jsonify({"message":"Assign project not found"}), 404
