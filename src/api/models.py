from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    last_name= db.Column(db.String(60), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    img_profile = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "img_profile":self.img_profile
            # do not serialize the password, its a security breach
        }

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    img_profile = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Administrator {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "img_profile": self.img_profile,
        }


db = SQLAlchemy()

### 🔹 MODELO DE FUNDACIONES ###
class Foundation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # ⚠️ Luego encriptaremos esto
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    img_profile = db.Column(db.String(255), nullable=True)

    # Relación con mascotas
    pets = db.relationship('Pet', backref='foundation', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f'<Foundation {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "img_profile": self.img_profile,
        }


### 🔹 MODELO DE MASCOTAS ###
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    is_adopted = db.Column(db.Boolean, default=False, nullable=False)


    # Relación con Foundation (clave foránea)
    foundation_id = db.Column(db.Integer, db.ForeignKey('foundation.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Pet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "description": self.description,
            "image": self.image,
            "is_adopted": self.is_adopted,
            "foundation_id": self.foundation_id,
            "foundation_name": self.foundation.name if self.foundation else None,
        }

