from pymongo import MongoClient, errors
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

# ----------MANAGER CLASS----------
class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    #Método para establecer la conexión con MongoDB Atlas
    def connect(self):
        # Obtener la configuración de la aplicación Flask
        config = current_app.config

        # Construir la URI de conexión utilizando los valores de la configuración
        username = config['MONGODB_USERNAME']
        password = config['MONGODB_PASSWORD']
        cluster = config['MONGODB_CLUSTER']
        dbname = config['MONGODB_DBNAME']
        uri = f"mongodb+srv://{username}:{password}@{cluster}/{dbname}?retryWrites=true&w=majority"

        # Establecer la conexión con MongoDB Atlas
        self.client = MongoClient(uri)
        self.db = self.client[dbname]

    #Método para obtener la instancia de la base de datos
    def get_db(self):
        if self.db is None:
            self.connect()
        return self.db

    #Método para crear una colección en la base de datos
    def create_collection(self, name, validator=None):
        db = self.get_db()
        if name not in db.list_collection_names():
            try:
                db.create_collection(name, validator=validator)
            except errors.CollectionInvalid:
                pass

    #Método para eliminar una colección de la base de datos
    def delete_collection(self, name):
        db = self.get_db()
        if name in db.list_collection_names():
            db[name].drop()

#Clase para manejar la colección de users
class UserManager:
    def __init__(self, mongodb_manager):
        self.db_manager = mongodb_manager
        self.reset_users_collection()

    #Método para reiniciar la colección de users
    def reset_users_collection(self):
        self.db_manager.delete_collection("users")
        validator = {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ["nombre", "password", "email", "rol"],
                'properties': {
                    'nombre': {
                        'bsonType': 'string',
                        'description': "Debe ser una cadena de caracteres para el nombre de usuario."
                    },
                    'password': {
                        'bsonType': 'string',
                        'description': "Debe ser una cadena de caracteres para la contraseña."
                    },
                    'email': {
                        'bsonType': 'string',
                        'description': "Debe ser una cadena de caracteres para el email."
                    },
                    'rol': {
                        'bsonType': 'string',
                        'description': "Debe ser una cadena de caracteres para el rol."
                    },
                }
            }
        }
        self.db_manager.create_collection("users", validator=validator)

# ----------MODELS CLASS----------
#CLASE CON METODOS PARA MANIPULAR USUARIOS
class Usuario:
    def __init__(self, nombre, password=None, email=None, rol=None, _id=None, password_hash=None):
        self._id = _id
        self.nombre = nombre
        if password:
            self.set_password(password)
        elif password_hash:
            self.password_hash = password_hash
        self.email = email
        self.rol = "paciente"

    #Método para establecer la contraseña del usuario
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #Método para verificar la contraseña del usuario
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Método para buscar un usuario por nombre
    @classmethod
    def find_by_name(cls, nombre):
        db = MongoDBManager().get_db()
        users_collection = db["users"]
        usuario = users_collection.find_one({'nombre': nombre})
        if usuario:
            return cls(
                nombre=usuario['nombre'],
                password_hash=usuario['password'],  # Hashed password
                email=usuario['email'],
                rol=usuario['rol'],
                _id=usuario['_id']  # Pasamos el ID aquí
            )
        return None

    #Método para guardar un usuario en la base de datos
    def save(self):
        db = MongoDBManager().get_db()
        users_collection = db["users"]

        user_data = {
            'nombre': self.nombre,
            'password': self.password_hash,  # Utilizamos el hash de la contraseña
            'email': self.email,
            'rol': self.rol,
        }

        if self._id:
            users_collection.update_one({'_id': self._id}, {'$set': user_data})
        else:
            result = users_collection.insert_one(user_data)
            self._id = result.inserted_id
    
    #Método para convertir el objeto a un diccionario
    def to_dict(self):
        return {
            "_id": str(self._id),
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
        }

    #Método para buscar un usuario por ID
    @classmethod
    def find_by_id(cls, user_id):
        db = MongoDBManager().get_db()
        user_data = db["users"].find_one({"_id": user_id})
        if user_data:
            return cls(**user_data)
        return None