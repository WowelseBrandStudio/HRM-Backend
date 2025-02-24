
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Manager
from Utils.helper import create_response, roles_accepted, serialize_user


class Managers:
    def __init__(self):
        pass

    @roles_accepted('Admin')    
    def insert_manager(self):

        data = request.form.to_dict()       
        
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
        manager = Manager.objects().order_by('-created_at').first() 
        if manager:
            unique_id =manager['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f'{'WOW-MAN-'}{new_number}'
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-MAN-1001'

        manager = Manager(**data)
        manager.save()
        return create_response(True,"Manager retrevied successfully",str(manager.id),None,201)

    
    @roles_accepted('Admin')
    def update_manager(self):
  
        data = request.form.to_dict()       

        id = data.get("id")       
        data['modified_at'] = datetime.datetime.now

        manager = Manager.objects(id=id).first()
        if not manager:
            return create_response(True,"Manager not found successfully",None,None,404)

    
        data.pop('id')  
        manager.update(**data)
        return create_response(True,"Manager updated successfully",str(manager.id),None,200)

    
    @roles_accepted('Admin','Manager')    
    def get_all_manager(self):

        manager = Manager.objects()
        res_data = [serialize_user(record) for record in manager]
        return create_response(True,"Manager retrevied successfully",res_data,None,200)

    
    @roles_accepted('Admin')    
    def delete_manager(self):
    
        data = request.get_json()
        id = data.get("id")
        manager = Manager.objects(id=id).delete()
        if manager == 1:
            return create_response(True,"Manager Deleted successfully",None,None,200)

        else:
            return create_response(True,"Manager not found",None,None,200)

