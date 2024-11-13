# API/models/user.py

from pymongo import MongoClient, errors
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from config import get_db

class User:
    def __init__(self, rut, nombre, apellidos, email, sexo, fecha_nacimiento, telefono_movil, tipo='patient', password=None, _id=None):
        self._id = _id
        self.rut = rut
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono_movil = telefono_movil
        self.tipo = tipo
        self.password_hash = generate_password_hash(password) if password else None

    @classmethod
    def login(cls, rut, password, expected_type):
        db = get_db()
        user_data = db["users"].find_one({"rut": rut})

        # Verificar si el usuario existe, la contraseña coincide y el tipo es el esperado
        if (
            user_data
            and user_data.get("password")
            and check_password_hash(user_data["password"], password)
            and user_data.get("tipo") == expected_type
        ):
            return True
        return False

    @classmethod
    def register(cls, rut, nombre, apellidos, email, sexo, fecha_nacimiento, telefono_movil, tipo='patient', password=None):
        db = get_db()
        
        # Verificar si el usuario ya existe por RUT
        if db["users"].find_one({"rut": rut}):
            return {"error": "El usuario con este RUT ya existe"}, 400

        # Crear el hash de la contraseña si se proporciona
        password_hash = generate_password_hash(password) if password else None
        new_user = {
            "rut": rut,
            "nombre": nombre,
            "apellidos": apellidos,
            "email": email,
            "sexo": sexo,
            "fecha_nacimiento": fecha_nacimiento,
            "telefono_movil": telefono_movil,
            "tipo": tipo,
            "password": password_hash
        }
        result = db["users"].insert_one(new_user)

        # Retornar la respuesta con los datos del usuario registrado
        return {
            "message": "Registro exitoso",
            "user": {
                "rut": rut,
                "nombre": nombre,
                "apellidos": apellidos,
                "email": email,
                "sexo": sexo,
                "fecha_nacimiento": fecha_nacimiento,
                "telefono_movil": telefono_movil,
                "tipo": tipo,
                "_id": str(result.inserted_id)
            }
        }, 201

    @classmethod
    def reset(cls):
        db = get_db()
        
        # Eliminar la colección si existe
        if "users" in db.list_collection_names():
            db["users"].drop()

        # Definir el esquema de validación JSON Schema
        user_schema = {
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ["rut", "nombre", "apellidos", "email", "sexo", "fecha_nacimiento", "telefono_movil", "tipo"],
                    'properties': {
                        'rut': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para el RUT del usuario."
                        },
                        'nombre': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para el nombre del usuario."
                        },
                        'apellidos': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para los apellidos del usuario."
                        },
                        'email': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para el correo electrónico del usuario."
                        },
                        'sexo': {
                            'bsonType': 'string',
                            'enum': ['M', 'F', 'Otro'],
                            'description': "El sexo debe ser 'M', 'F' u 'Otro'."
                        },
                        'fecha_nacimiento': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para la fecha de nacimiento en formato ISO."
                        },
                        'telefono_movil': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para el número de teléfono móvil del usuario."
                        },
                        'tipo': {
                            'bsonType': 'string',
                            'enum': ['patient', 'specialist', 'admin'],
                            'description': "El tipo de usuario debe ser 'patient', 'specialist' o 'admin'."
                        },
                        'password': {
                            'bsonType': 'string',
                            'description': "Debe ser una cadena de caracteres para la contraseña en hash del usuario."
                        }
                    }
                }
            }
        }

        # Crear la colección con el esquema de validación
        try:
            db.create_collection("users", **user_schema)
        except errors.CollectionInvalid:
            db.command({
                'collMod': 'users',
                'validator': user_schema['validator']
            })

        return {"message": "La colección de usuarios ha sido restablecida con el esquema especificado"}, 200

    def set_password(self, password):
        """
        Establece o cambia la contraseña del usuario.
        """
        self.password_hash = generate_password_hash(password)
        db = get_db()
        db["users"].update_one({"rut": self.rut}, {"$set": {"password": self.password_hash}})

    def save(self):
        db = get_db()
        user_data = {
            "rut": self.rut,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "sexo": self.sexo,
            "fecha_nacimiento": self.fecha_nacimiento,
            "telefono_movil": self.telefono_movil,
            "tipo": self.tipo,
            "password": self.password_hash
        }
        if self._id:
            db["users"].update_one({"_id": self._id}, {"$set": user_data})
        else:
            result = db["users"].insert_one(user_data)
            self._id = result.inserted_id

    def to_dict(self):
        return {
            "_id": str(self._id),
            "rut": self.rut,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "sexo": self.sexo,
            "fecha_nacimiento": self.fecha_nacimiento,
            "telefono_movil": self.telefono_movil,
            "tipo": self.tipo
        }
