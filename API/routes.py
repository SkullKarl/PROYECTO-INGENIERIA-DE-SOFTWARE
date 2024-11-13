from flask import Blueprint, jsonify, request
from models import MongoDBManager, Usuario, UserManager

api_bp = Blueprint('api', __name__)

#RUTAS DE USUARIO
class UserHandler:
    #Metodo para registrar un nuevo usuario
    @staticmethod
    def register():
        data = request.json
        required_fields = ["nombre", "password", "email"]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Datos incompletos"}), 400

        existing_user = Usuario.find_by_name(data["nombre"])
        if existing_user:
            return jsonify({"error": "Ya existe un usuario con este nombre"}), 400

        user = Usuario(
            nombre=data["nombre"],
            password=data["password"],
            email=data["email"]
        )
        user.save()

        user_info = {
            "_id": str(user._id),
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol,
        }
        return jsonify({"mensaje": "Usuario registrado con éxito", "usuario": user_info}), 201

    #Metodo para resetear la coleccion de usuarios
    @staticmethod
    def reset_users():
        db_manager = MongoDBManager()
        user_manager = UserManager(db_manager)
        return jsonify({"mensaje": "La colección de users ha sido restablecida"}), 200

    # Método para buscar usuarios que sean especialistas
    @staticmethod
    def get_specialist_users():
        db = MongoDBManager().get_db()
        users_collection = db["users"]

        users = users_collection.find({"rol": {"$regex": "especialista", "$options": "i"}})
        user_list = [
            {
                "_id": str(user["_id"]),
                "nombre": user["nombre"],
                "email": user["email"],
                "rol": user["rol"]
            } for user in users
        ]
        return jsonify({"especialistas": user_list}), 200

    # Método para buscar usuarios por rol
    @staticmethod
    def get_users_by_role():
        role = request.args.get('rol')

        if not role:
            return jsonify({"error": "Se requiere especificar un rol"}), 400

        db = MongoDBManager().get_db()
        users_collection = db["users"]

        users = users_collection.find({"rol": role})
        user_list = [
            {
                "_id": str(user["_id"]),
                "nombre": user["nombre"],
                "email": user["email"],
                "rol": user["rol"]
            } for user in users
        ]

        return jsonify({"usuarios": user_list}), 200

api_bp.add_url_rule('/', view_func=lambda: 'Ejecutando API')

#Rutas de Usuario
api_bp.add_url_rule('/reset_users', view_func=UserHandler.reset_users, methods=['POST'])
api_bp.add_url_rule('/register', view_func=UserHandler.register, methods=['POST'])
api_bp.add_url_rule('/users_by_role', view_func=UserHandler.get_users_by_role, methods=['GET'])
api_bp.add_url_rule('/specialists', view_func=UserHandler.get_specialist_users, methods=['GET'])