# API/routes/specialist_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from models.specialist import Specialist

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
