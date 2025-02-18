
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Manager
from Utils.helper import serialize_user


class Managers:
    def __init__(self):
        pass

    
    def insert_manager(self):

        data = request.form.to_dict()       
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['created_by'] = '1'
        data['created_by_role'] = 'test'

        manager = Manager(**data)
        manager.save()
        return jsonify({"message":"Manager created successfully"}),201
    
    def update_manager(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
        
        if data.get('gender') !=  None:
            if data.get('gender') not in possible_gender:
                return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['modified_at'] = datetime.datetime.now

        manager = Manager.objects(id=id).first()
        if not manager:
            return jsonify({"message":"Manager not found"}), 404
    
        data.pop('id')  
        manager.update(**data)
        return jsonify({"message": "Manager updated successfully"}),200
    
        
    def get_all_manager(self):

        manager = Manager.objects()
        res_data = [serialize_user(record) for record in manager]
        return jsonify({"message": "Manager retrevied successfully", "data": res_data}),200
    
        
    def delete_manager(self):
    
        data = request.get_json()
        id = data.get("id")
        manager = Manager.objects(id=id).first()
        if not manager:
            return jsonify({"message":"Manager not found"}), 404
        
        manager.delete()    
        return jsonify({"message":"Manager Deleted successfully"}), 200