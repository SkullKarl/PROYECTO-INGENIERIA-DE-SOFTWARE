# API/routes/patient_routes.py

from flask import Blueprint, request, jsonify
from API.models.user import User
from API.config import get_db

# Creación del Blueprint para las rutas de pacientes
patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = User.register(
        rut=data.get('rut'),
        nombre=data.get('nombre'),
        apellidos=data.get('apellidos'),
        email=data.get('email'),
        sexo=data.get('sexo'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        telefono_movil=data.get('telefono_movil'),
        tipo='patient',
        password=data.get('password')
    )
    return jsonify(response)

@patient_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    # Llamada al método de login del modelo User con el tipo de usuario 'patient'
    login_successful = User.login(rut, password, expected_type='patient')
    return jsonify({"login_successful": login_successful})

@patient_bp.route('/reset', methods=['POST'])
def reset():
    response = User.reset()
    return jsonify(response)

# Método para buscar usuarios que sean especialistas
@staticmethod
def get_specialist_users():
    db = get_db()
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
    db = get_db()
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