# API/routes/specialist_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from models.specialist import Specialist
from config import get_db
from bson import ObjectId

# Creación del Blueprint para las rutas de especialistas
specialist_bp = Blueprint('specialist', __name__)

@specialist_bp.route('/register', methods=['POST'])
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
        tipo='specialist',
        password=data.get('password')
    )
    return jsonify(response)

@specialist_bp.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión como especialista y devuelve la información del usuario si el inicio de sesión es exitoso.
    """
    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    if not rut or not password:
        return jsonify({"error": "Se requiere RUT y contraseña"}), 400

    # Llamada al método de login del modelo User con el tipo de usuario 'specialist'
    login_successful = User.login(rut, password, expected_type='specialist')

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
@specialist_bp.route('/reset', methods=['POST'])
def reset():
    response = User.reset()
    return jsonify(response)

@specialist_bp.route("/get_appointments", methods=["POST"])
def get_appointments_by_specialist():
    """
    Obtiene todas las citas asociadas a un especialista dado su RUT.
    """
    data = request.get_json()
    specialist_rut = data.get("rut")

    if not specialist_rut:
        return jsonify({"error": "Debe proporcionar el RUT del especialista"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    # Buscar todas las citas asociadas al RUT del especialista
    appointments = list(appointments_collection.find({"specialist_rut": specialist_rut}))

    if not appointments:
        return jsonify({"message": "No se encontraron citas para este especialista"}), 404

    # Convertir ObjectId a cadenas y construir la respuesta
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):  # ObjectId debe estar importado
            return str(obj)
        return obj

    appointments_data = convert_objectid(appointments)

    return jsonify({"appointments": appointments_data}), 200


@specialist_bp.route('/add_block', methods=['POST'])
def add_block():
    data = request.get_json()
    rut = data.get('rut')
    day = data.get('day')
    hour = data.get('hour')

    if not rut or day is None or hour is None:
        return jsonify({"error": "Se requieren 'rut', 'day' y 'hour'"}), 400

    specialist = Specialist(rut=rut)
    response = specialist.add_block(day, hour)
    return jsonify(response)

@specialist_bp.route('/set_specialty', methods=['POST'])
def set_specialty():
    """
    Ruta para actualizar la especialidad de un especialista dado su rut.
    """
    data = request.get_json()
    rut = data.get('rut')
    specialty = data.get('specialty')

    if not rut or not specialty:
        return jsonify({"error": "Se requieren 'rut' y 'specialty'"}), 400

    specialist = Specialist(rut=rut)
    response = specialist.set_specialty(specialty)
    return jsonify(response)

@specialist_bp.route("/get_timetable", methods=["Post"])
def get_timetable():
    """
    Obtiene el horario asociado a un especialista dado su rut.
    """
    data = request.get_json()
    rut = data.get("rut")

    if not rut:
        return jsonify({"error": "Debe proporcionar un RUT para buscar el horario"}), 400

    db = get_db()
    doctors_collection = db["doctors"]

    # Buscar el especialista en la colección `doctors`
    doctor = doctors_collection.find_one({"rut": rut}, {"available_blocks": 1, "_id": 0})

    if not doctor:
        return jsonify({"error": "No se encontró un especialista con el RUT proporcionado"}), 404

    # Extraer los bloques disponibles y organizarlos
    available_blocks = doctor.get("available_blocks", [])
    timetable = []

    for block in available_blocks:
        day, hour = block.split("-")
        timetable.append({"day": int(day), "hour": int(hour)})

    return jsonify({"rut": rut, "timetable": sorted(timetable, key=lambda x: (x["day"], x["hour"]))}), 200