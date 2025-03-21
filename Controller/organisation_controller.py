from flask import g, request

from Models.ModelSchemas import HOST, organization
from Utils.helper import create_response, serialize_user
from mongoengine import connect, disconnect


class Organization:
    def __init__(self):
        pass
        # db_name = g.payload['app_id']
        
        # disconnect('default')
        # self.connect_to_db(db_name)
      

    def connect_to_db(self, db_name):
        # Dynamically switch the database based on app_id
        connect(
            host = HOST,
            db = db_name,
        )
    
    def insert_organization(self):
        """
        1. Insert organization information
        """
        data = request.get_json()
        data.update({
            "api_key": "123",
            "api_secret": "123",
            "app_id": "abc"
        })
        # collection_name = data.get('app_id', 'default_collection')  # Default fallback if app_name is missing
        # self.meta = {'collection': collection_name}
        res_obj = organization(**data)
        res_obj.save()
        return create_response(True,"Organization added successfully",str(res_obj.id),None,201)

    
    def update_organization(self):
        """
        1. Update organization information
        """
        data = request.get_json()
        id = data.get("id")
        res_obj = organization.objects(id=id).update(**data)
        return create_response(True,"Organization updated successfully",str(res_obj.id),None,200)

    
    def delete_organization(self):
        """
        1. Delete organization information
        """
        data = request.get_json()
        id = data.get("id")
        res_obj = organization.objects(id=id).delete()
        return create_response(True,"Organization deleted successfully",None,None,200)

    
    def get_organization_by_id(self):
        """
        1. Retrieve organization information by id
        """
        data = request.args.to_dict()
        id = data.get("id")
        res_obj = organization.objects(id=id).first()
        if not res_obj:
            return create_response(True,"Organization not found",None,None,404)
        return create_response(True,"Organization retrieved successfully",res_obj,None,200)

    