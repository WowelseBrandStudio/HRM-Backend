
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Bonus
from Utils.helper import create_response, roles_accepted, serialize_user


class Bonus_tip:
    def __init__(self):
        pass

    @roles_accepted('HR')    
    def insert_bonus(self):
       
        data = request.get_json()

        bonus = Bonus(**data).save()
        return create_response(True,"Bonus created successfully",str(bonus.id),None,201)
    
    @roles_accepted('HR')   
    def update_bonus(self):
  
        data = request.get_json()    
        id = data.get('id')
        data['modified_at'] = datetime.datetime.now

        bonus = Bonus.objects(id=id).first()
        if not bonus:
            return create_response(True,"Bonus notsuccessfully",None,None,404)

    
        data.pop('id')  
        bonus.update(**data)
        return create_response(True,"Bonus updated successfully",str(bonus.id),None,200)
    
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
        return create_response(True,"Bonus retrevied successfully",res_data,None,200)
    
    @roles_accepted('HR')  
    def delete_bonus(self):
    
        data = request.get_json()
        id = data.get("id")
        bonus = Bonus.objects(id=id).delete()
        if bonus == 1 :
            return create_response(True,"Bonus Deleted successfully",None,None,200)            
        else:
            return create_response(False,"Bonus not found",None,None,200)
