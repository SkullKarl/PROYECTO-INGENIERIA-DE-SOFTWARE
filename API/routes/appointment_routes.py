# API/routes/appointment_routes.py

from bson import ObjectId
from flask import Blueprint, request, jsonify
from models.appointment import Appointment

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/schedule', methods=['POST'])
def schedule_appointment():
    data = request.get_json()

    paciente_rut = data.get('paciente_rut')
    especialista_rut = data.get('specialist_rut')
    fecha = data.get('fecha')
    hora = data.get('hora')

    if not all([paciente_rut, especialista_rut, fecha, hora]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Llamada a la función de reserva de cita
    response = Appointment.schedule(paciente_rut, especialista_rut, fecha, hora)

    # Si response contiene un ObjectId, conviértelo a str antes de enviarlo
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    # Convierte todos los ObjectId a cadenas
    response_data = convert_objectid(response[0])

    return jsonify(response_data), response[1]