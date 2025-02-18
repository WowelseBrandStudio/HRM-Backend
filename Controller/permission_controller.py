
from flask import jsonify, request
from Models.ModelSchemas import permission_request
from Utils.helper import serialize_user


class Permission:
    def __init__(self):
        pass

    def get_permission_requested_list(self):
        res_obj = permission_request.objects()
        res_data = [serialize_user(record) for record in res_obj]
        return jsonify({"message": "Permission request", "data": res_data})

    def request_permission(self):
        """
        1. User can request for permission | (insert the information in collection)
        """
        data = request.get_json()
        res_obj = permission_request(**data)
        res_obj.save()
        return {"message": "Permission request submitted successfully."}
    
    def update_permission(self):
        """
        1. Admin can update permission request status | (Approve the permission or not)
        """
        data = request.get_json()
        permission_id = data.get("_id")
        res_obj = permission_request.objects(id=permission_id).first()
        data.pop('_id', None)   # _id cant update
        res_obj.update(**data)
        return {"message": "Permission request updated successfully."}
    
    def delete_permission(self):
        """
        1. Admin can delete permission request | (Remove the permission request from collection)
        """
        data = request.get_json()
        permission_id = data.get("_id")
        # import pdb; pdb.set_trace()
        res_obj = permission_request.objects(id=permission_id).first()
        res_obj.delete()
        return {"message": "Permission request deleted successfully."}
    