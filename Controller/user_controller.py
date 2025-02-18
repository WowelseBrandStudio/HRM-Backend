
import datetime
from flask import jsonify, request
from Models.ModelSchemas import User
from Utils.helper import serialize_user


class Users:
    def __init__(self):
        pass

    
    def insert_user(self):

        data = request.form.to_dict()       
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['created_by'] = '1'
        data['created_by_role'] = 'test'

        user = User(**data)
        user.save()
        return jsonify({"message":"User created successfully"}),201
    
    def update_user(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
        
        if data.get('gender') !=  None:
            if data.get('gender') not in possible_gender:
                return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['modified_at'] = datetime.datetime.now

        user = User.objects(id=id).first()
        if not user:
            return jsonify({"message":"User not found"}), 404
    
        data.pop('id')  
        user.update(**data)
        return jsonify({"message": "User updated successfully"}),200
    
        
    def get_all_user(self):

        user = User.objects()
        res_data = [serialize_user(record) for record in user]
        return jsonify({"message": "User retrevied successfully", "data": res_data}),200
    
        
    def delete_user(self):
    
        data = request.get_json()
        id = data.get("id")
        user = User.objects(id=id).first()
        if not user:
            return jsonify({"message":"User not found"}), 404
        
        user.delete()    
        return jsonify({"message":"User Deleted successfully"}), 200