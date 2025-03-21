
import datetime
from flask import g,render_template, request
from Controller.email_controller import send_mail
from Models.ModelSchemas import HOST, Human_resource
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist

class Human_resources:
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


    @roles_accepted('Admin','Manager')
    
    def insert_hr(self):

        data = request.form.to_dict()       
       
        client_data = g.payload
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        
        hr = Human_resource.objects().order_by('-created_at').first() 
        if hr:
            unique_id =hr['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f"{'WOW-HR-'}{new_number}"
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-HR-1001'

        hr = Human_resource(**data)
        hr.save()

        html_template = render_template('registration_template.html',email=data.get('email'),password=data.get('password'),login_url='http://localhost:4200/auth/sign-in/HR')
        send_mail(data.get('email'),"Registration successfull",html_template,'hrm25085@gmail.com')
        
        return create_response(True,"Hr created successfully",str(hr.id),None,201)
        

    
    @roles_accepted('Admin','Manager')
    def update_hr(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
       
        data['modified_at'] = datetime.datetime.now

        hr = Human_resource.objects(id=id).first()
       
        if not hr:
            raise DoesNotExist(f'HR {id} not found') 

        data.pop('id')          
        hr.update(**data)
        return create_response(True,"Hr updated successfully",None,None,200)

    
    @roles_accepted('Admin', 'HR','Manager')    
    def get_all_hr(self):
        data = request.args.to_dict()     

        client_data=g.payload
    
        if client_data['role'] == 'HR':
            hr_id =client_data['user_id']
        else:            
            hr_id =  data.get('hr_id') 
                
        user_filter={
            'id':hr_id
        } if hr_id else {}
        
        hr = Human_resource.objects(**user_filter)

        res_data = [serialize_user(record) for record in hr]
        return create_response(True,"Hr retrevied successfully",res_data,None,200)

    
    @roles_accepted('Admin','Manager')    
    def delete_hr(self):
    
        data = request.get_json()
        id = data.get("id")
        hr = Human_resource.objects(id=id).delete()
        
        if hr == 1:
            return create_response(True,"Hr Deleted successfully",None,None,200)

        else:
            return create_response(True,"Hr not found",None,None,404)
