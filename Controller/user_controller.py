
import datetime
from flask import g, jsonify, request
from Models.ModelSchemas import Employee
from Utils.helper import roles_accepted, serialize_user


class Employees:
    def __init__(self):
        pass

    @roles_accepted('Admin', 'HR','Manager')    
    def insert_employee(self):
        
        data = request.form.to_dict()  
       
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
       
        user = Employee.objects().order_by('-created_at').first() 
        if user:
            unique_id =user['user_id']
            sliced_unique_id = unique_id.split('-')[-1]
            new_number = int(sliced_unique_id)+1
            new_unique_id = f'{'WOW-EMP-'}{new_number}'
            data['user_id'] = new_unique_id
        else:
            data['user_id'] = 'WOW-EMP-1001'

        user = Employee(**data)
        user.save()
        return jsonify({"message":"Employee created successfully"}),201
    
    @roles_accepted('Admin', 'HR','Manager')
    def update_employee(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        data['modified_at'] = datetime.datetime.now

        user = Employee.objects(id=id).first()
        if not user:
            return jsonify({"message":"Employee not found"}), 404
    
        data.pop('id')  
        user.update(**data)
        return jsonify({"message": "Employee updated successfully"}),200
    
    @roles_accepted('Admin', 'HR', 'User','Manager')
    def get_all_employee(self):
        client_data=g.client_data
        filter = request.args.to_dict()
        roles = {
            'Manager': lambda: filter.update({"responsible_manager": client_data['user_id']}),
            'HR': lambda: filter.update({"responsible_hr": client_data['user_id']}),
            'User': lambda: filter.update({"id": client_data['user_id']})
            # 'Admin': lambda: filter.update({})
        }
        roles.get(client_data['role'], lambda: None)()
        user = Employee.objects(**filter)
        res_data = [serialize_user(record) for record in user]
        return jsonify({"message": "Employee retrevied successfully", "data": res_data}),200
    
    @roles_accepted('Admin', 'HR','Manager')
    def delete_employee(self):
    
        data = request.get_json()
        id = data.get("id")
        user = Employee.objects(id=id).delete()
        if user == 1 :
            return jsonify({"message":"Employee Deleted successfully"}), 200
        else:
            return jsonify({"message":"Employee not found"}), 404  