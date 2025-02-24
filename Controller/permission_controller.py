
from flask import g, jsonify, request
from Models.ModelSchemas import HOST, permission_request
from Utils.helper import create_response, roles_accepted, serialize_user
from mongoengine import connect, disconnect

class Permission:
    def __init__(self):
        db_name = g.payload['app_id']
        disconnect('default')
        self.connect_to_db(db_name)
        print("connected to db : ", g.payload['app_id'])

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )


    @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_permission_requested_list(self):
        res_obj = permission_request.objects()
        res_data = [serialize_user(record) for record in res_obj]
        
        return create_response(True,"Permission request",res_data,None,200)


    @roles_accepted('HR', 'User','Manager')
    def request_permission(self):
        """
        1. User can request for permission | (insert the information in collection)
        """
        data = request.get_json()
        res_obj = permission_request(**data)
        res_obj.save()
        return create_response(True,"Permission request submitted",str(res_obj.id),None,201)

    
    @roles_accepted('HR', 'User','Manager')
    def update_permission(self):
        """
        1. Admin can update permission request status | (Approve the permission or not)
        """
        data = request.get_json()
        permission_id = data.get("_id")
        res_obj = permission_request.objects(id=permission_id).first()
        data.pop('_id', None)   # _id cant update
        res_obj.update(**data)
        return create_response(True,"Permission request updated",str(res_obj.id),None,200)


    @roles_accepted('HR', 'User','Manager')    
    def delete_permission(self):
        """
        1. Admin can delete permission request | (Remove the permission request from collection)
        """
        data = request.get_json()
        permission_id = data.get("_id")
        # import pdb; pdb.set_trace()
        res_obj = permission_request.objects(id=permission_id).first()
        res_obj.delete()
        return create_response(True,"Permission request deleted successfully",None,None,200)

    