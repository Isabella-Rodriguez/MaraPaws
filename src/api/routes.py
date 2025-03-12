"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
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


