
from flask import g
from Models.ModelSchemas import HOST, Admin, Employee, Human_resource, Manager
from Utils.helper import create_response, serialize_user
from mongoengine import connect, disconnect



class UserInfo:
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

    def user_info(self):
            client_data=g.payload
            user_id=client_data['user_id']

            if client_data['role'] == 'Admin':
                collection_name = Admin
            elif client_data['role'] == 'User':
                collection_name = Employee
            elif client_data['role'] == 'Manager':
                collection_name = Manager
            else:
                collection_name = Human_resource

            user = collection_name.objects(id=user_id)
        
            res_data = [serialize_user(record) for record in user]
            return create_response(True,"Data retrevied successfully",res_data,None,200)



class Dashboard:
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

    def dashboard_count(self):
            client_data=g.payload
            
            res_data={}
            if client_data['role'] == 'Admin':
                res_data['hr_count'] = len(Human_resource.objects())
                res_data['manager_count'] = len(Manager.objects())
                res_data['employee_count'] = len(Employee.objects())
        
            elif client_data['role'] == 'Manager':
                res_data['hr_count'] = len(Human_resource.objects())
                res_data['employee_count'] = len(Employee.objects(responsible_manager = client_data['user_id']))

                # Manager count not necessary for manager role
                res_data['manager_count'] = 0  

            elif client_data['role'] == 'HR':
                res_data['employee_count'] = len(Employee.objects(responsible_hr=client_data['user_id']))

                # Manager and hr count not necessary for hr role
                res_data['manager_count'] = 0
                res_data['hr_count'] = 0

            
            return create_response(True,"Data retrevied successfully",res_data,None,200)