
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Admin
from Utils.helper import roles_accepted, serialize_user


class Admins:
    def __init__(self):
        pass

    @roles_accepted('Admin')    
    def insert_admin(self):

        data = request.form.to_dict()        

        admin = Admin.objects().order_by('-created_at').first()     
        if admin:
            unique_id =admin['user_id']            
            sliced_unique_id = unique_id[8:12]      
            new_unique_id = f'{'WOW-ADM-'}{sliced_unique_id}'
            data['user_id'] = new_unique_id

        else:
            data['user_id'] = 'WOW-ADM-1001'
       
        admin = Admin(**data)
        admin.save()
        return jsonify({"message":"Admin created successfully"}),201
    
    @roles_accepted('Admin')
    def update_admin(self):
  
        data = request.form.to_dict()      
        id = data.get("id")
        admin = Admin.objects(id=id).first()
        if not admin:
            return jsonify({"message":"Admin not found"}), 404
    
        data.pop('id')  
        admin.update(**data)
        return jsonify({"message": "Admin updated successfully"}),200
    
    @roles_accepted('Admin')    
    def get_all_admin(self):
       
        client_data=g.client_data        
        user_id =client_data['user_id']
        
        admin = Admin.objects(id = user_id)
        res_data = [serialize_user(record) for record in admin]
        return jsonify({"message": "admin retrevied successfully", "data": res_data}),200
    
    @roles_accepted('Admin')  
    def delete_admin(self):
    
        data = request.get_json()
        id = data.get("id")
        admin = Admin.objects(id=id).delete()
        if admin == 1:
            return jsonify({"message":"admin Deleted successfully"}), 200
        else:
            return jsonify({"message":"admin not found"}), 404