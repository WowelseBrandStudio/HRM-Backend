from flask import request

from Models.ModelSchemas import organization
from Utils.helper import serialize_user


class Organization:
    def __init__(self):
        pass
    
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
        return {"message": "Organization added successfully."}
    
    def update_organization(self):
        """
        1. Update organization information
        """
        data = request.get_json()
        id = data.get("id")
        res_obj = organization.objects(id=id).update(**data)
        return {"message": "Organization updated successfully."}
    
    def delete_organization(self):
        """
        1. Delete organization information
        """
        data = request.get_json()
        id = data.get("id")
        res_obj = organization.objects(id=id).delete()
        return {"message": "Organization deleted successfully."}
    
    def get_organization_by_id(self):
        """
        1. Retrieve organization information by id
        """
        data = request.args.to_dict()
        id = data.get("id")
        res_obj = organization.objects(id=id).first()
        # res_data = [serialize_user(record) for record in res_obj]
        if not res_obj:
            return {"message": "Organization not found."}, 404
        return {"message": "Organization retrieved successfully", "data": res_obj}
    