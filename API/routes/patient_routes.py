# API/routes/patient_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from config import get_db

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

@patient_bp.route("/get_by_name", methods=["GET"])
def get_by_name():
    data = request.get_json()
    nombre = data.get("nombre")
    db = get_db()
    users_collection = db["users"]
    user = users_collection.find_one({"nombre": nombre})
    usuario = {
        "rut": user["rut"],
        "nombre": user["nombre"],
        "apellidos": user["apellidos"],
        "email": user["email"],
        "sexo": user["sexo"],
        "fecha nacimiento": user["fecha_nacimiento"],
        "telefono movil": user["telefono_movil"]
    }
    if usuario:
        return jsonify(usuario), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@patient_bp.route("/get_by_specialty", methods=['GET'])
def get_by_specialty():
    data = request.get_json()
    specialty = data.get("specialty")
    if not specialty:
        return jsonify({"Error": "Se requiere especificar una especialidad"}), 400
    db = get_db()
    users_collection = db["users"]
    users = users_collection.find({"specialty": specialty})
    specialty_user_list = [
        {
            "rut": user["rut"],
            "nombre": user["nombre"],
            "apellidos": user["apellidos"],
            "email": user["email"],
            "sexo": user["sexo"],
            "fecha nacimiento": user["fecha_nacimiento"],
            "telefono movil": user["telefono_movil"]
        } for user in users
    ]
    return jsonify({"Especialistas": specialty_user_list}), 200

@patient_bp.route("/get_specialists_users", methods=["GET"])
def get_specialists_users():
    db = get_db()
    users_collection = db["users"]
    specialists_users = users_collection.find({"tipo": {"$regex": "specialist", "$options": "i"}})
    specialists_user_list = [
        {
            "rut": user["rut"],
            "nombre": user["nombre"],
            "apellidos": user["apellidos"],
            "email": user["email"],
            "sexo": user["sexo"],
            "fecha nacimiento": user["fecha_nacimiento"],
            "telefono movil": user["telefono_movil"]
        } for user in specialists_users
    ]
    return jsonify({"Especialistas": specialists_user_list}), 200

@patient_bp.route("/get_medical_center_info", methods=["GET"])
def get_medical_center_info():
    return jsonify("Informacion del centro medico: hola"), 200