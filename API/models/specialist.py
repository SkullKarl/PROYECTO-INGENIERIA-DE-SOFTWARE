# API/models/specialist.py

from pymongo import errors
from config import get_db

class Specialist:
    def __init__(self, rut):
        self.rut = rut

    def add_block(self, day, hour):
        """
        Asocia un bloque de tiempo al especialista basado en la combinación única de day y hour.
        """
        db = get_db()

        # Buscar el bloque en la colección `blocks` mediante `day` y `hour`
        block = db["blocks"].find_one({"day": day, "hour": hour})
        if not block:
            return {"error": "El bloque especificado no existe"}, 404

        # Crear una representación única del bloque con day y hour
        block_identifier = f"{day}-{hour}"

        # Verificar si el especialista ya tiene un documento en `doctors` usando su `rut`
        doctor_record = db["doctors"].find_one({"rut": self.rut})
        
        if doctor_record:
            # Si el especialista ya tiene bloques, agregamos el nuevo bloque si no está duplicado
            if block_identifier in doctor_record["available_blocks"]:
                return {"error": "El bloque ya está asociado a este especialista"}, 400
            db["doctors"].update_one(
                {"rut": self.rut},
                {"$push": {"available_blocks": block_identifier}}
            )
        else:
            # Crear un nuevo registro para el especialista con el bloque
            db["doctors"].insert_one({
                "rut": self.rut,
                "available_blocks": [block_identifier]
            })

        return {"message": "Bloque agregado al horario del especialista"}, 201
    
    def set_specialty(self, specialty):
        """
        Cambia la especialidad del doctor dado su rut.
        """
        db = get_db()
        
        # Actualizar la especialidad en el documento del doctor
        result = db["doctors"].update_one(
            {"rut": self.rut},
            {"$set": {"specialty": specialty}}
        )
        
        if result.matched_count == 0:
            return {"error": "Doctor no encontrado"}, 404

        return {"message": f"Especialidad actualizada a {specialty}"}, 200