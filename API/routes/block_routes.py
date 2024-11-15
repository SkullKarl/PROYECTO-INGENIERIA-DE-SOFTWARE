# API/routes/block_routes.py

from flask import Blueprint, jsonify
from models.block import Block

# Creación del Blueprint para las rutas de bloques
block_bp = Blueprint('block', __name__)

@block_bp.route('/reset', methods=['POST'])
def reset_blocks():
    """
    Resetea la colección de bloques eliminando todos los documentos.
    """
    response = Block.reset()
    return jsonify(response)

@block_bp.route('/generate', methods=['POST'])
def generate_blocks():
    """
    Genera todos los bloques posibles de lunes a sábado, de 8 AM a 5 PM.
    """
    response = Block.generate()
    return jsonify(response)
