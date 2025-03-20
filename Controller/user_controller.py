
import datetime
from flask import g, jsonify, render_template, request
from Controller.email_controller import send_mail
from Models.ModelSchemas import HOST, Employee
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist


class Employees:
    def __init__(self):
        db_name = g.payload['app_id']
        disconnect('default')
        self.connect_to_db(db_name)      

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )

    @roles_accepted('Admin', 'HR','Manager')    
    def insert_employee(self):
        
        data = request.form.to_dict()  
       
        client_data = g.payload
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
       
        user = Employee.objects().order_by('-created_at').first() 
        if user:
            unique_id =user['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f"{'WOW-EMP-'}{new_number}"
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-EMP-1001'

        user = Employee(**data)
        user.save()
        
        html_template = render_template('registration_template.html',email=data.get('email'),password=data.get('password'),login_url='http://localhost:4200/auth/sign-in/User')
        send_mail(data.get('email'),"Registration successfull",html_template,'hrm25085@gmail.com')
        
        return create_response(True,"Employee created successfully",str(user.id),None,201)

    
    @roles_accepted('Admin', 'HR','Manager')
    def update_employee(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        data['modified_at'] = datetime.datetime.now

        user = Employee.objects(id=id).first()
        if not user:
            raise DoesNotExist(f'Employee {id} not found') 

        data.pop('id')  
        user.update(**data)
        return create_response(True,"Employee updated successfully",str(user.id),None,200)

    
    # @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_employee(self):
        
        client_data=g.payload
        filter = request.args.to_dict()
        
        roles = {
            'Manager': lambda: filter.update({"responsible_manager": client_data['user_id']}),
            'HR': lambda: filter.update({"responsible_hr": client_data['user_id']}),
            'User': lambda: filter.update({"id": client_data['user_id']})
            # 'Admin': lambda: filter.update({})
        }
       
        roles.get(client_data['role'], lambda: None)()
        user = Employee.objects(**filter)
       
        res_data = [serialize_user(record) for record in user]
        return create_response(True,"Employee retrevied successfully",res_data,None,200)

    
    @roles_accepted('Admin', 'HR','Manager')
    def delete_employee(self):
    
        data = request.get_json()
        id = data.get("id")
        user = Employee.objects(id=id).delete()
        if user == 1 :
            return create_response(True,"Employee Deleted successfully",None,None,200)

        else:
            return create_response(True,"Employee not found",None,None,200)
