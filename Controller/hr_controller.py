
import datetime
from flask import jsonify, request
from Models.ModelSchemas import Human_resource
from Utils.helper import serialize_user


class Human_resources:
    def __init__(self):
        pass

    
    def insert_hr(self):

        data = request.form.to_dict()       
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['created_by'] = '1'
        data['created_by_role'] = 'test'

        hr = Human_resource(**data)
        hr.save()
        return jsonify({"message":"Hr created successfully"}),201
    
    def update_hr(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
        
        if data.get('gender') !=  None:
            if data.get('gender') not in possible_gender:
                return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['modified_at'] = datetime.datetime.now

        hr = Human_resource.objects(id=id).first()
        if not hr:
            return jsonify({"message":"Hr not found"}), 404
    
        data.pop('id')  
        hr.update(**data)
        return jsonify({"message": "Hr updated successfully"}),200
    
        
    def get_all_hr(self):

        hr = Human_resource.objects()
        res_data = [serialize_user(record) for record in hr]
        return jsonify({"message": "Hr retrevied successfully", "data": res_data}),200
    
        
    def delete_hr(self):
    
        data = request.get_json()
        id = data.get("id")
        hr = Human_resource.objects(id=id).first()
        if not hr:
            return jsonify({"message":"Hr not found"}), 404
        
        hr.delete()    
        return jsonify({"message":"Hr Deleted successfully"}), 200