# API/routes/specialist_routes.py

from flask import Blueprint, request, jsonify
from models.user import User

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
