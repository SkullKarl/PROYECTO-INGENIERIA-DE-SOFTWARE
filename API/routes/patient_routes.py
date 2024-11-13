# API/routes/patient_routes.py

from flask import Blueprint, request, jsonify
from models.user import User

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
