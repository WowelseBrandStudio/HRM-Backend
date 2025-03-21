
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import HOST, Admin
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect,DoesNotExist


class Admins:
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
    def insert_admin(self):

        data = request.form.to_dict()        

        admin = Admin.objects().order_by('-created_at').first()     
        if admin:
            unique_id =admin['user_id']            
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f"{'WOW-ADM-'}{new_number}"
            data['user_id'] = new_unique_id

        else:
            data['user_id'] = 'WOW-ADM-1001'
       
        admin = Admin(**data)
        admin.save()   
       
        return create_response(True,"Admin created successfully",str(admin.id),None,201)

    
    @roles_accepted('Admin')
    def update_admin(self):
  
        data = request.form.to_dict()      
        client_data=g.payload        
        id =client_data['user_id']
        admin = Admin.objects(id=id).first()
        if not admin:
            raise DoesNotExist(f'Admin {id} not found') 
            
        admin.update(**data)
        
        return create_response(True,"Admin updated successfully",str(admin.id),None,200)
    
    @roles_accepted('Admin')    
    def get_all_admin(self):
       
        client_data=g.payload        
        user_id =client_data['user_id']   
        
        admin = Admin.objects(id = user_id)
        res_data = [serialize_user(record) for record in admin]
     
        return create_response(True,"Admin retrevied successfully",res_data,None,200)
    
    @roles_accepted('Admin')  
    def delete_admin(self):
    
        client_data=g.payload        
        id =client_data['user_id']
        
        admin = Admin.objects(id=id).delete()
        if admin == 1:
           
            return create_response(True,"Admin Deleted successfully",None,None,200)

        else:
          
            return create_response(True,"Admin not found",None,"Data not found",404)
