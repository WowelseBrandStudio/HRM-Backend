
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Human_resource
from Utils.helper import roles_accepted, serialize_user


class Human_resources:
    def __init__(self):
        pass

    @roles_accepted('Admin','Manager')
    
    def insert_hr(self):

        data = request.form.to_dict()       
       
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        
        hr = Human_resource.objects().order_by('-created_at').first() 
        if hr:
            unique_id =hr['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f'{'WOW-HR-'}{new_number}'
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-HR-1001'

        hr = Human_resource(**data)
        hr.save()
        return jsonify({"message":"Hr created successfully"}),201
    
    @roles_accepted('Admin','Manager')
    def update_hr(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
       
        data['modified_at'] = datetime.datetime.now

        hr = Human_resource.objects(id=id).first()
        if not hr:
            return jsonify({"message":"Hr not found"}), 404
    
        data.pop('id')  
        hr.update(**data)
        return jsonify({"message": "Hr updated successfully"}),200
    
    @roles_accepted('Admin', 'HR','Manager')    
    def get_all_hr(self):

        hr = Human_resource.objects()
        res_data = [serialize_user(record) for record in hr]
        return jsonify({"message": "Hr retrevied successfully", "data": res_data}),200
    
    @roles_accepted('Admin','Manager')    
    def delete_hr(self):
    
        data = request.get_json()
        id = data.get("id")
        hr = Human_resource.objects(id=id).delete()
        
        if hr == 1:
            return jsonify({"message":"Hr Deleted successfully"}), 200
        else:
            return jsonify({"message":"Hr not found"}), 404
