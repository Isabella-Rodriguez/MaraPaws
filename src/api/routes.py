"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User, Administrator
from api.utils import APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

### 🔹 ENDPOINTS PARA USERS ###
@api.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()

    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400 

    print(body) 

    user = User.query.filter_by(email=body["email"]).first()
    print(user)
    if user is None: 
        user = User(
            name=body["name"],
            last_name=body["last_name"],
            email=body["email"],  
            password=body["password"], 
            is_active=True
        )
        db.session.add(user)
        db.session.commit()

        response_body = {
            "msg": "usuario creado"
        }
        return jsonify(response_body), 201  
    else:
        return jsonify({"msg": "ya hay un usuario con ese email"}), 

@api.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = [user.serialize() for user in all_users]
    return jsonify(results), 200


### 🔹 OBTENER UN USUARIO POR ID ###
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify(user.serialize()), 200


### 🔹 EDITAR UN USUARIO POR ID ###
@api.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    body = request.get_json()

    user.name = body.get("name", user.name)
    user.last_name = body.get("last_name", user.last_name)
    user.email = body.get("email", user.email)
    user.password = body.get("password", user.password)  # ⚠️ Luego se debe encriptar
    user.is_active = body.get("is_active", user.is_active)

    db.session.commit()

    return jsonify({"msg": "Usuario actualizado", "user": user.serialize()}), 200


### 🔹 ELIMINAR UN USUARIO POR ID ###
@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "Usuario eliminado"}), 200



### 🔹 CREAR UN ADMINISTRADOR ###
@api.route('/administrators', methods=['POST'])
def create_administrator():
    body = request.get_json()

    if not body:
        return jsonify({"msg": "No se recibió ningún dato"}), 400  

    admin = Administrator.query.filter_by(email=body["email"]).first()
    if admin is None: 
        admin = Administrator(
            name=body["name"],
            last_name=body["last_name"],
            email=body["email"],  
            password=body["password"],  # ⚠️ Luego encriptaremos esto
            is_active=True,
            img_profile=body.get("img_profile", "")
        )
        db.session.add(admin)
        db.session.commit()

        return jsonify({"msg": "Administrador creado"}), 201  
    else:
        return jsonify({"msg": "Ya hay un administrador con ese email"}), 409


### 🔹 OBTENER TODOS LOS ADMINISTRADORES ###
@api.route('/administrators', methods=['GET'])
def get_administrators():
    all_admins = Administrator.query.all()
    results = [admin.serialize() for admin in all_admins]
    return jsonify(results), 200


### 🔹 OBTENER UN ADMINISTRADOR POR ID ###
@api.route('/administrators/<int:admin_id>', methods=['GET'])
def get_administrator(admin_id):
    admin = Administrator.query.get(admin_id)
    if not admin:
        return jsonify({"msg": "Administrador no encontrado"}), 404

    return jsonify(admin.serialize()), 200


### 🔹 EDITAR UN ADMINISTRADOR POR ID ###
@api.route('/administrators/<int:admin_id>', methods=['PUT'])
def update_administrator(admin_id):
    admin = Administrator.query.get(admin_id)
    if not admin:
        return jsonify({"msg": "Administrador no encontrado"}), 404

    body = request.get_json()

    admin.name = body.get("name", admin.name)
    admin.last_name = body.get("last_name", admin.last_name)
    admin.email = body.get("email", admin.email)
    admin.password = body.get("password", admin.password)  # ⚠️ Luego encriptaremos esto
    admin.is_active = body.get("is_active", admin.is_active)

    db.session.commit()

    return jsonify({"msg": "Administrador actualizado", "admin": admin.serialize()}), 200


### 🔹 ELIMINAR UN ADMINISTRADOR POR ID ###
@api.route('/administrators/<int:admin_id>', methods=['DELETE'])
def delete_administrator(admin_id):
    admin = Administrator.query.get(admin_id)
    if not admin:
        return jsonify({"msg": "Administrador no encontrado"}), 404

    db.session.delete(admin)
    db.session.commit()

    return jsonify({"msg": "Administrador eliminado"}), 200


