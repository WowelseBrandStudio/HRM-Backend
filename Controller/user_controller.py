
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
       
        possible_gender =['Male','Female','Others']

        if data.get('gender') not in possible_gender:
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        client_data = g.client_data
        data['created_by'] = client_data['user_id']
        data['created_by_role'] = client_data['role']
       
        user = Employee.objects().order_by('-created_at').first() 
        if user:
            unique_id =user['unique_id']
            sliced_unique_id = unique_id[8:12] + 1
            new_unique_id = f'{'WOW-EMP-'}{sliced_unique_id}'
            data['unique_id'] = new_unique_id
        else:
            data['unique_id'] = 'WOW-EMP-1001'

        user = Employee(**data)
        user.save()
        return jsonify({"message":"Employee created successfully"}),201
    
    @roles_accepted('Admin', 'HR','Manager')
    def update_employee(self):
  
        data = request.form.to_dict()       

        id = data.get("id")
        possible_gender =['Male','Female','Others']
     
        if data.get('gender') !=  None and data.get('gender') not in possible_gender:           
            return jsonify({"message":"invalid gender","avaialble_gender":possible_gender})
        
        data['modified_at'] = datetime.datetime.now

        user = Employee.objects(id=id).first()
        if not user:
            return jsonify({"message":"Employee not found"}), 404
    
        data.pop('id')  
        user.update(**data)
        return jsonify({"message": "Employee updated successfully"}),200
    
    @roles_accepted('Admin', 'HR', 'User','Manager')     
    def get_all_employee(self):

        user = Employee.objects()
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