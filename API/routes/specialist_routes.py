# API/routes/specialist_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from models.specialist import Specialist
from config import get_db

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
    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    # Llamada al método de login del modelo User con el tipo de usuario 'specialist'
    login_successful = User.login(rut, password, expected_type='specialist')
    return jsonify({"login_successful": login_successful})

@specialist_bp.route('/reset', methods=['POST'])
def reset():
    response = User.reset()
    return jsonify(response)

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


