# API/models/block.py

from pymongo import errors
from config import get_db

class Block:
    @classmethod
    def reset(cls):
        """
        Elimina todos los documentos en la colección 'blocks'.
        """
        db = get_db()
        db["blocks"].delete_many({})
        return {"message": "La colección de bloques ha sido reseteada"}, 200

    @classmethod
    def generate(cls):
        """
        Genera todos los bloques posibles (de lunes a sábado, de 8 AM a 5 PM).
        """
        db = get_db()

        # Rango de días (lunes a sábado) y horas (de 8 AM a 5 PM)
        days = range(1, 7)  # 1: lunes, 6: sábado
        hours = range(8, 21)  # 8 AM a 5 PM (17:00 inclusive)

        # Lista para almacenar los bloques a insertar
        blocks = []
        
        for day in days:
            for hour in hours:
                block = {
                    "day": day,
                    "hour": hour
                }
                blocks.append(block)

        # Insertar todos los bloques generados en la colección
        db["blocks"].insert_many(blocks)
        return {"message": "Todos los bloques posibles han sido generados"}, 201
