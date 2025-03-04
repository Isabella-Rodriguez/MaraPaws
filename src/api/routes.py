"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User, Administrator, Foundation, Pet
from api.utils import APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

### 🔹 ENDPOINTS PARA USERS ###
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data or not all(key in data for key in ["name", "last_name", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(
        name=data["name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],
        is_active=True,
        img_profile=data.get("img_profile", "")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])  # Solo este endpoint permite DELETE
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

### 🔹 ENDPOINTS PARA ADMINISTRATORS ###
@api.route('/administrators', methods=['POST'])
def create_administrator():
    data = request.json

    if not data or not all(key in data for key in ["name", "last_name", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_admin = Administrator(
        name=data["name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],
        is_active=True,
        img_profile=data.get("img_profile", "")
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify(new_admin.serialize()), 201

@api.route('/administrators', methods=['GET'])
def get_administrators():
    admins = Administrator.query.all()
    return jsonify([admin.serialize() for admin in admins]), 200

### 🔹 ENDPOINTS PARA FOUNDATIONS ###
@api.route('/foundations', methods=['POST'])
def create_foundation():
    data = request.json

    if not data or not all(key in data for key in ["name", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_foundation = Foundation(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        is_active=True,
        img_profile=data.get("img_profile", "")
    )

    db.session.add(new_foundation)
    db.session.commit()

    return jsonify(new_foundation.serialize()), 201

@api.route('/foundations', methods=['GET'])
def get_foundations():
    foundations = Foundation.query.all()
    return jsonify([foundation.serialize() for foundation in foundations]), 200

### 🔹 ENDPOINTS PARA PETS ###
@api.route('/pets', methods=['POST'])
def create_pet():
    data = request.json

    if not data or not all(key in data for key in ["name", "age", "foundation_id"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_pet = Pet(
        name=data["name"],
        age=data["age"],
        description=data.get("description", ""),
        image=data.get("image", ""),
        foundation_id=data["foundation_id"]
    )

    db.session.add(new_pet)
    db.session.commit()

    return jsonify(new_pet.serialize()), 201

@api.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([pet.serialize() for pet in pets]), 200

@api.route('/pets/<int:pet_id>', methods=['PUT'])  # Solo este endpoint permite PUT
def update_pet(pet_id):
    pet = Pet.query.get(pet_id)

    if not pet:
        return jsonify({"error": "Pet not found"}), 404

    data = request.json

    pet.name = data.get("name", pet.name)
    pet.age = data.get("age", pet.age)
    pet.description = data.get("description", pet.description)
    pet.image = data.get("image", pet.image)

    db.session.commit()

    return jsonify({"message": "Pet updated successfully", "pet": pet.serialize()}), 200
