
import datetime
from flask import g, jsonify, render_template, request
from Controller.email_controller import send_mail
from Models.ModelSchemas import HOST, Manager
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist


class Managers:
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

    @roles_accepted('Admin')    
    def insert_manager(self):

        data = request.form.to_dict()       
        
        client_data = g.payload
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        manager = Manager.objects().order_by('-created_at').first() 
        if manager:
            unique_id =manager['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f"{'WOW-MAN-'}{new_number}"
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-MAN-1001'

        manager = Manager(**data)
        manager.save()
                
        html_template = render_template('registration_template.html',email=data.get('email'),password=data.get('password'),login_url='http://hrm-wowelse.s3-website-us-east-1.amazonaws.com/auth/sign-in/Manager')
        send_mail(data.get('email'),"Registration successfull",html_template,'hrm25085@gmail.com')
        
        return create_response(True,"Manager created successfully",str(manager.id),None,201)

    
    @roles_accepted('Admin')
    def update_manager(self):
  
        data = request.form.to_dict()       

        id = data.get("id")       
        data['modified_at'] = datetime.datetime.now

        manager = Manager.objects(id=id).first()
        if not manager:
            raise DoesNotExist(f'Manager {id} not found') 

    
        data.pop('id')  
        manager.update(**data)
        return create_response(True,"Manager updated successfully",str(manager.id),None,200)

    
    @roles_accepted('Admin','Manager')    
    def get_all_manager(self):
        data = request.args.to_dict()     
        
        client_data=g.payload
    
        if client_data['role'] == 'Manager':
            manager_id =client_data['user_id']
        else:            
            manager_id =  data.get('manager_id') 
                
        user_filter={
            'id':manager_id
        } if manager_id else {}
        
        manager = Manager.objects(**user_filter)

        res_data = [serialize_user(record) for record in manager]
        return create_response(True,"Manager retrevied successfully",res_data,None,200)

    
    @roles_accepted('Admin')    
    def delete_manager(self):
    
        data = request.get_json()
        id = data.get("id")
        manager = Manager.objects(id=id).delete()
        if manager == 1:
            return create_response(True,"Manager Deleted successfully",None,None,200)

        else:
            return create_response(True,"Manager not found",None,None,200)

