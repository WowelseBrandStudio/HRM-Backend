
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import HOST, Project
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist


class Projects:
    def __init__(self):
        pass
        # db_name = g.payload['app_id']
        
        # disconnect('default')
        # self.connect_to_db(db_name)
      

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )

    @roles_accepted('Admin', 'HR','Manager')    
    def insert_project(self):

        data = request.get_json()       
       
        client_data = g.payload
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
            raise DoesNotExist(f'Project {id} not found')           
    
        data.pop('id')  
        project.update(**data)
        return create_response(True,"Project updated successfull",str(project.id),None,200)

    
    # @roles_accepted('Admin', 'HR', 'User','Manager')    
    def get_all_project(self):

        project = Project.objects()
        res_data = [serialize_user(record) for record in project]
        return create_response(True,"Project retrevied successfully",res_data,None,200)

    
    # @roles_accepted('Admin', 'HR', 'User','Manager')    
    def delete_project(self):
    
        data = request.get_json()
        id = data.get("id")
        project = Project.objects(id=id).delete()
        if project == 1:
            return create_response(True,"Project Deleted  successfully",None,None,200)

        else:
            return create_response(True,"Project not found",None,None,404)
