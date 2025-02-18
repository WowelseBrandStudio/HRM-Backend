
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Admin
from Utils.helper import serialize_user


class Admins:
    def __init__(self):
        pass

    
    def insert_admin(self):

        data = request.form.to_dict()           
        admin = Admin(**data)
        admin.save()
        return jsonify({"message":"Admin created successfully"}),201
    
    def update_admin(self):
  
        data = request.form.to_dict()      
        id = data.get("id")
        admin = Admin.objects(id=id).first()
        if not admin:
            return jsonify({"message":"Admin not found"}), 404
    
        data.pop('id')  
        admin.update(**data)
        return jsonify({"message": "Admin updated successfully"}),200
    
        
    def get_all_admin(self):

        admin = Admin.objects()
        res_data = [serialize_user(record) for record in admin]
        return jsonify({"message": "admin retrevied successfully", "data": res_data}),200
    
        
    def delete_admin(self):
    
        data = request.get_json()
        id = data.get("id")
        admin = Admin.objects(id=id).first()
        if not admin:
            return jsonify({"message":"admin not found"}), 404
        
        admin.delete()    
        return jsonify({"message":"admin Deleted successfully"}), 200