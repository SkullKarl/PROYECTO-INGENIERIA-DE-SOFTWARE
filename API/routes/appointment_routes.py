# API/routes/appointment_routes.py

from bson import ObjectId
from flask import Blueprint, request, jsonify
from models.appointment import Appointment
from config import get_db

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

# Obtener todas las citas
@appointment_bp.route('/List', methods=['GET'])
def get_all_appointments():
    db = get_db()
    appointments_collection = db["appointment"]
    
    appointments = list(appointments_collection.find())
    
    # Convertir todos los ObjectId a cadenas
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    appointments_data = convert_objectid(appointments)
    
    return jsonify(appointments_data), 200

# Elimina una cita de la base de datos
@appointment_bp.route('/delete', methods=['POST'])
def delete_appointment():
    """
    Elimina una cita de la base de datos.
    """
    data = request.get_json()
    appointment_id = data.get('appointment_id')

    if not appointment_id:
        return jsonify({"error": "El campo 'appointment_id' es requerido"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    try:
        # Convertir el ID a ObjectId
        appointment_id = ObjectId(appointment_id)

        # Eliminar la cita de la base de datos
        result = appointments_collection.delete_one({"_id": appointment_id})

        if result.deleted_count == 0:
            return jsonify({"error": "Cita no encontrada"}), 404

        return jsonify({"message": "Cita eliminada exitosamente"}), 200

    except (TypeError, ValueError):
        return jsonify({"error": "ID inválido"}), 400

# Cancela una cita actualizando su estado
@appointment_bp.route('/cancel', methods=['POST'])
def cancel_appointment():

    data = request.get_json()
    appointment_id = data.get('appointment_id')

    if not appointment_id:
        return jsonify({"error": "El campo 'appointment_id' es requerido"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    try:
        # Convertir el ID a ObjectId
        appointment_id = ObjectId(appointment_id)

        # Actualizar el estado de la cita
        result = appointments_collection.update_one(
            {"_id": appointment_id},
            {"$set": {"estado": "cancelado"}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Cita no encontrada"}), 404

        return jsonify({"message": "Cita cancelada exitosamente"}), 200

    except (TypeError, ValueError):
        return jsonify({"error": "ID inválido"}), 400


# Modifica una cita
@appointment_bp.route('/modify', methods=['PUT'])
def modify_appointment():

    data = request.get_json()
    appointment_id = data.get('appointment_id')
    nueva_fecha = data.get('fecha')
    nueva_hora = data.get('hora')

    if not appointment_id or not nueva_fecha or not nueva_hora:
        return jsonify({"error": "Se requieren 'appointment_id', 'fecha' y 'hora'"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    try:
        # Convertir el ID a ObjectId
        appointment_id = ObjectId(appointment_id)

        # Verificar si ya existe otra cita en el nuevo horario
        conflicto = appointments_collection.find_one({
            "fecha": nueva_fecha,
            "hora": nueva_hora
        })
        if conflicto and str(conflicto["_id"]) != appointment_id:
            return jsonify({"error": "Ya existe una cita en la fecha y hora especificadas"}), 409

        # Actualizar la cita
        result = appointments_collection.update_one(
            {"_id": appointment_id},
            {"$set": {"fecha": nueva_fecha, "hora": nueva_hora}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Cita no encontrada"}), 404

        return jsonify({"message": "Cita modificada exitosamente"}), 200

    except (TypeError, ValueError):
        return jsonify({"error": "ID inválido"}), 400
    

# Obtener una cita por ID
@appointment_bp.route('/Get_by_id', methods=['POST'])
def get_appointment_by_id():

    data = request.get_json()
    appointment_id = data.get('appointment_id')

    if not appointment_id:
        return jsonify({"error": "El campo 'appointment_id' es requerido"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    try:
        appointment_id = ObjectId(appointment_id)
        appointment = appointments_collection.find_one({"_id": appointment_id})
        if not appointment:
            return jsonify({"error": "Cita no encontrada"}), 404

        # ... (resto del código para convertir ObjectId a str y retornar la respuesta)

    except (TypeError, ValueError):
        return jsonify({"error": "ID invalido"}), 400
    
    # Convertir todos los ObjectId a cadenas
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    appointments_data = convert_objectid(appointment)
    
    return jsonify(appointments_data), 200

    # Obtener todas las citas de un médico específico

@appointment_bp.route('/ListByDoctor', methods=['POST'])
def get_appointments_by_doctor():
    """
    Obtiene todas las citas asociadas a un médico específico identificado por su RUT.
    """
    data = request.get_json()
    doctor_rut = data.get("rut")

    if not doctor_rut:
        return jsonify({"error": "Debe proporcionar el RUT del médico"}), 400

    db = get_db()
    appointments_collection = db["appointment"]

    # Buscar citas asociadas al RUT del médico
    appointments = list(appointments_collection.find({"specialist_rut": doctor_rut}))

    # Convertir todos los ObjectId a cadenas
    def convert_objectid(obj):
        if isinstance(obj, dict):
            return {key: convert_objectid(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_objectid(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    appointments_data = convert_objectid(appointments)

    if not appointments_data:
        return jsonify({"message": "No se encontraron citas para el médico especificado"}), 404

    return jsonify(appointments_data), 200
