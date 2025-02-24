
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Project
from Utils.helper import create_response, roles_accepted, serialize_user


class Projects:
    def __init__(self):
        pass

    @roles_accepted('Admin', 'HR','Manager')    
    def insert_project(self):

        data = request.get_json()       
       
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']

        project = Project(**data)
        project.save()
        return create_response(True,"Project created successfully",str(project.id),None,201)

    
    @roles_accepted('Admin', 'HR','Manager')
    def update_project(self):
  
        data = request.get_json()

        id = data.get("id")
        
        data['modified_at'] = datetime.datetime.now
       
        project = Project.objects(id=id).first()
        if not project:
            return create_response(True,"Project not found",None,None,404)
    
        data.pop('id')  
        project.update(**data)
        return create_response(True,"Project updated successfull",str(project.id),None,200)

    
    @roles_accepted('Admin', 'HR', 'User','Manager')    
    def get_all_project(self):

        project = Project.objects()
        res_data = [serialize_user(record) for record in project]
        return create_response(True,"Project retrevied successfully",res_data,None,200)

    
    @roles_accepted('Admin', 'HR', 'User','Manager')    
    def delete_project(self):
    
        data = request.get_json()
        id = data.get("id")
        project = Project.objects(id=id).delete()
        if project == 1:
            return create_response(True,"Project Deleted  successfully",None,None,200)

        else:
            return create_response(True,"Project not found",None,None,404)
