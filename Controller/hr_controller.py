
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
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        
        hr = Human_resource.objects().order_by('-created_at').first() 
        if hr:
            unique_id =hr['unique_id']
            sliced_unique_id = unique_id[9:12] + 1
            new_unique_id = f'{'WOW-HR-'}{sliced_unique_id}'
            data['unique_id'] = new_unique_id
        else:
            data['unique_id'] = 'WOW-HR-1001'

        hr = Human_resource(**data)
        hr.save()
        return jsonify({"message":"Hr created successfully"}),201
    
    @roles_accepted('Admin','Manager')
    def update_hr(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
        
        if data.get('gender') != None and data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
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
