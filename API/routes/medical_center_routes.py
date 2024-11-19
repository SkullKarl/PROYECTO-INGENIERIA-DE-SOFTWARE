from flask import Blueprint, request, jsonify
from config import get_db

medical_center_bp = Blueprint('medical_center', __name__)

# Filtra centros médicos
@medical_center_bp.route('/filter', methods=['POST'])
def filter_medical_centers():

    data = request.get_json()
    nombre = data.get('nombre')
    ubicacion = data.get('ubicacion')
    especialidad = data.get('especialidad')

    db = get_db()
    medical_centers_collection = db["medical_centers"]

    # Construir la consulta dinámica
    query = {}
    if nombre:
        query["nombre"] = {"$regex": nombre, "$options": "i"}  # Búsqueda insensible a mayúsculas/minúsculas
    if ubicacion:
        query["ubicacion"] = {"$regex": ubicacion, "$options": "i"}
    if especialidad:
        query["especialidades"] = {"$in": [especialidad]}  # Busca si la especialidad está en la lista

    # Obtener los resultados de la base de datos
    results = list(medical_centers_collection.find(query, {"_id": 0}))  # Excluir el campo `_id` en la respuesta

    return jsonify(results), 200
