# API/routes/patient_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from config import get_db
from bson import ObjectId

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
    """
    Inicia sesión como paciente y devuelve la información del usuario si el inicio de sesión es exitoso.
    """
    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    if not rut or not password:
        return jsonify({"error": "Se requiere RUT y contraseña"}), 400

    # Llamada al método de login del modelo User con el tipo de usuario 'patient'
    login_successful = User.login(rut, password, expected_type='patient')

    if not login_successful:
        return jsonify({"login_successful": False, "error": "Credenciales incorrectas"}), 401

    # Buscar la información completa del usuario en la base de datos
    db = get_db()
    user_data = db["users"].find_one({"rut": rut}, {
        "rut": 1,
        "nombre": 1,
        "apellidos": 1,
        "email": 1,
        "sexo": 1,
        "fecha_nacimiento": 1,
        "telefono_movil": 1,
        "_id": 0  # Excluir el campo _id
    })

    if not user_data:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Retornar login exitoso junto con la información del usuario
    return jsonify({
        "login_successful": True,
        "user": user_data
    }), 200

@patient_bp.route('/reset', methods=['POST'])
def reset():
    response = User.reset()
    return jsonify(response)

@patient_bp.route("/get_by_name", methods=["POST"])
def get_by_name():
    """
    Busca un usuario por su nombre en la colección `users`.
    """
    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Debe proporcionar un nombre para buscar"}), 400

    db = get_db()
    users_collection = db["users"]
    user = users_collection.find_one({"nombre": nombre})

    if not user:
        return jsonify({"error": "Usuario con el nombre especificado no encontrado"}), 404

    usuario = {
        "rut": user["rut"],
        "nombre": user["nombre"],
        "apellidos": user["apellidos"],
        "email": user["email"],
        "sexo": user["sexo"],
        "fecha nacimiento": user["fecha_nacimiento"],
        "telefono movil": user["telefono_movil"]
    }

    return jsonify(usuario), 200

@patient_bp.route("/get_by_specialty", methods=['POST'])
def get_by_specialty():
    """
    Obtiene especialistas por especialidad buscando primero en `doctors` y luego en `users`.
    """
    data = request.get_json()
    specialty = data.get("specialty")

    if not specialty:
        return jsonify({"Error": "Se requiere especificar una especialidad"}), 400

    db = get_db()

    # Buscar en la colección `doctors` todos los ruts con la especialidad solicitada
    doctors_collection = db["doctors"]
    doctors = doctors_collection.find({"specialty": specialty}, {"rut": 1, "_id": 0})
    ruts = [doctor["rut"] for doctor in doctors]

    if not ruts:
        return jsonify({"Especialistas": []}), 200

    # Buscar en la colección `users` la información de los ruts obtenidos
    users_collection = db["users"]
    users = users_collection.find({"rut": {"$in": ruts}})
    
    # Construir la lista de especialistas con los datos de `users`
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

@patient_bp.route("/get_appointments", methods=["POST"])
def get_appointments_by_patient():
    """
    Obtiene todas las citas asociadas a un paciente dado su RUT.
    """
    data = request.get_json()
    paciente_rut = data.get("rut")

    if not paciente_rut:
        return jsonify({"error": "Debe proporcionar el RUT del paciente"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    # Buscar todas las citas asociadas al RUT del paciente
    appointments = list(appointments_collection.find({"paciente_rut": paciente_rut}))

    if not appointments:
        return jsonify({"message": "No se encontraron citas para este paciente"}), 404

    # Convertir ObjectId a cadenas y construir la respuesta
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    appointments_data = convert_objectid(appointments)

    return jsonify({"appointments": appointments_data}), 200