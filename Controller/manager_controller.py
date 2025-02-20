
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Manager
from Utils.helper import roles_accepted, serialize_user


class Managers:
    def __init__(self):
        pass

    @roles_accepted('Admin')    
    def insert_manager(self):

        data = request.form.to_dict()       
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        manager = Manager.objects().order_by('-created_at').first() 
        if manager:
            unique_id =manager['unique_id']
            sliced_unique_id = unique_id[8:12] + 1
            new_unique_id = f'{'WOW-MAN-'}{sliced_unique_id}'
            data['unique_id'] = new_unique_id
        else:
            data['unique_id'] = 'WOW-MAN-1001'

        manager = Manager(**data)
        manager.save()
        return jsonify({"message":"Manager created successfully"}),201
    
    @roles_accepted('Admin')
    def update_manager(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
        
        if data.get('gender') !=  None and data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['modified_at'] = datetime.datetime.now

        manager = Manager.objects(id=id).first()
        if not manager:
            return jsonify({"message":"Manager not found"}), 404
    
        data.pop('id')  
        manager.update(**data)
        return jsonify({"message": "Manager updated successfully"}),200
    
    @roles_accepted('Admin','Manager')    
    def get_all_manager(self):

        manager = Manager.objects()
        res_data = [serialize_user(record) for record in manager]
        return jsonify({"message": "Manager retrevied successfully", "data": res_data}),200
    
    @roles_accepted('Admin')    
    def delete_manager(self):
    
        data = request.get_json()
        id = data.get("id")
        manager = Manager.objects(id=id).delete()
        if manager == 1:
            return jsonify({"message":"Manager Deleted successfully"}), 200
        else:
            return jsonify({"message":"Manager not found"}), 404
