from flask import Flask, jsonify, request
from mongoengine import connect, Document,DateField, StringField, EmailField, IntField,ListField, QuerySetManager, NotUniqueError, ValidationError, DoesNotExist
from bson import ObjectId

app = Flask(__name__)

connect(
    host = 'mongodb+srv://user:user@wowelse1.c179k.mongodb.net/?retryWrites=true&w=majority&appName=wowelse1',
    db='company'
)

@app.errorhandler(NotUniqueError)
def handle_duplicate_error(error):
    return {"error": str(error)}, 400

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return {"error": str(error)}, 400

@app.errorhandler(DoesNotExist)
def handle_not_found_error(error):
    return {"error": str(error)}, 404


@app.errorhandler(Exception)
def unknown_exception_err(error):
    return {"error": str(error)}, 500


def serialize_user(id):
    user_dict = id.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict


class Admin(Document):
    objects = QuerySetManager()
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    name =StringField(required=True,unique=True)
    email = EmailField(required=True)
    mobile = StringField(required=False)


@app.route('/admin', methods=['GET','POST','DELETE'])
def admin():
    methods = {
        'POST': insert_admin,
        'GET': get_admin,
        'DELETE': delete_admin,
    }
    return methods.get(request.method)()
        

def insert_admin():
    data = request.form.to_dict()
    user = Admin(**data)
    user.save()
    return jsonify({"message":"Admin created successfully"})


def get_admin():
    admins = Admin.objects()
    
    # # users = [user.to_json() for user in users]
    # users = [user.to_mongo().to_dict() for user in users]
    admins = [serialize_user(admin) for admin in admins]
    # for user in users:
    #     users['_id'] = str(user['_id'])

    response_data = {
            "success": True,
            "data": admins,
            "msg": "Success" if admins else "Record not found"
        }
    
    return jsonify(response_data), 200

def delete_admin():
   
    data = request.get_json()
    admin = Admin.objects(id=data.get("id"))
    if not user:
        return jsonify({"message":"Admin not found"}), 404
    
    admin.delete()    
    return jsonify({"message":"Deleted successfully"}), 200
  
class User(Document):
    objects = QuerySetManager()
   
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, unique=True)
    role = StringField(required=True)
    name = StringField(required=True)
    dob = DateField(required=True)
    area = StringField(required=True)
    state = StringField(required=True)
    pincode = IntField(required=True)   
    gender = StringField(required=False)
    # permissions = ListField(StringField())
    # newpassword = StringField()
    # created_at = DateTimeField(default=datetime.now())
    
@app.route('/user', methods=['GET','POST','DELETE',])
def user():
    methods = {
        'POST': insert_user,
        'GET': get_user,
        # 'PUT':update_user,
        'DELETE':delete_user
    }
    return methods.get(request.method)()


def insert_user():
    data =request.form.to_dict()
    user = User(**data)
    user.save()
    return jsonify({"message":"User created successfully"})



def get_user():
    users = User.objects()
   
    # # users = [user.to_json() for user in users]
    # users = [user.to_mongo().to_dict() for user in users]
    users = [serialize_user(user) for user in users]
    # for user in users:
    #     users['_id'] = str(user['_id'])

    response_data = {
            "success": True,
            "data": users,
            "msg": "Success" if users else "Record not found"
        }
    
    return jsonify(response_data), 200


def delete_user():
   
    data = request.get_json()
    user = User.objects(id=data.get("id"))
    if not user:
        return jsonify({"message":"User not found"}), 404

    user.delete()    
    return jsonify({"message":"Deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)



# DEPRECATED:
# res = serialize_single_user(users)
# "data": [serialize_user(user) for user in users]



# def serialize_single_user(user):
#     return {
#         "_id": str(user.id),  # Convert ObjectId to string
#         "username": user.username,
#         "email": user.email,
#         "role": user.role,
#         "permissions": user.permissions
#     } if user else None