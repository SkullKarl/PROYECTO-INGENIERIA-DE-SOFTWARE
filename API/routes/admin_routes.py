# API/routes/admin_routes.py

from flask import Blueprint, request, jsonify
from models.user import User

# Creación del Blueprint para las rutas de administradores
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/register', methods=['POST'])
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
        tipo='admin',
        password=data.get('password')
    )
    return jsonify(response)

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    rut = data.get('rut')
    password = data.get('password')

    # Llamada al método de login del modelo User con el tipo de usuario 'admin'
    login_successful = User.login(rut, password, expected_type='admin')
    return jsonify({"login_successful": login_successful})

@admin_bp.route('/reset', methods=['POST'])
def reset():
    response = User.reset()
    return jsonify(response)