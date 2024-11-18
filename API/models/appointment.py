# API/models/appointment.py

from pymongo.errors import DuplicateKeyError
from config import get_db


class Appointment:
    @classmethod
    def schedule(cls, paciente_rut, especialista_rut, fecha, hora):

        #Agenda una cita y vereficara con la base de datos de MongoDB si hay disponibilidad
        db = get_db()
        appointments_collection = db["appointment"]

        # Verificar si ya existe una cita en esa fecha y hora para el paciente
        existing_patient_appointment = appointments_collection.find_one({
            "paciente_rut": paciente_rut,
            "fecha": fecha,
            "hora": hora
        })
        if existing_patient_appointment:
            return {"error": "El paciente ya tiene una cita agendada para esta fecha y hora."}, 409

        # Verificar si ya existe una cita para el especialista en la misma fecha y hora
        existing_specialist_appointment = appointments_collection.find_one({
            "specialist_rut": especialista_rut,
            "fecha": fecha,
            "hora": hora
        })
        if existing_specialist_appointment:
            return {"error": "El especialista ya tiene una cita agendada para este horario."}, 409

        # Crear nueva cita
        appointment = {
            "paciente_rut": paciente_rut,
            "specialist_rut": especialista_rut,
            "fecha": fecha,
            "hora": hora,
            "estado": "agendado"  # Estado inicial de la cita
        }

        try:
            appointments_collection.insert_one(appointment)
            return {"mensage": "Cita agendada exitosamente", "appointment": appointment}, 201
        except DuplicateKeyError:
            return {"error": "Error al agendar la cita, conflicto en el identificador"}, 500