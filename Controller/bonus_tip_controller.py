
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Bonus
from Utils.helper import roles_accepted, serialize_user


class Bonus_tip:
    def __init__(self):
        pass

    @roles_accepted('HR')    
    def insert_bonus(self):
       
        data = request.get_json()

        bonus = Bonus(**data)
        bonus.save()
        return jsonify({"message":"Bonus created successfully"}),201
    
    @roles_accepted('HR')   
    def update_bonus(self):
  
        data = request.get_json()    
        id = data.get('id')
        data['modified_at'] = datetime.datetime.now

        bonus = Bonus.objects(id=id).first()
        if not bonus:
            return jsonify({"message":"Bonus not found"}), 404
    
        data.pop('id')  
        bonus.update(**data)
        return jsonify({"message": "Bonus updated successfully"}),200
    
    @roles_accepted('HR','User')  
    def get_all_bonus(self):
       
        data = request.args.to_dict()
        client_data=g.client_data
        if client_data['role'] == 'User':
            user_id =client_data['user_id']
        else:            
            user_id =  data.get('user_id') 
                
        user_filter={
            'user_id':user_id
        } if user_id else {}

        bonus = Bonus.objects(**user_filter)

        res_data = [serialize_user(record) for record in bonus]
        return jsonify({"message": "Bonus retrevied successfully", "data": res_data}),200
    
    @roles_accepted('HR')  
    def delete_bonus(self):
    
        data = request.get_json()
        id = data.get("id")
        bonus = Bonus.objects(id=id).delete()
        if bonus == 1 :
            return jsonify({"message":"Bonus Deleted successfully"}), 200
        else:
            return jsonify({"message":"Bonus not found"}), 404  