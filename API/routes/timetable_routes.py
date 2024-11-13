# API/routes/timetable_routes.py

from flask import Blueprint, jsonify
from models.block import Timetable

# Creación del Blueprint para las rutas de horarios
timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/reset', methods=['POST'])
def reset_timetable():
    response = Timetable.reset()
    return jsonify(response)

@timetable_bp.route('/generate', methods=['POST'])
def generate_timetable():
    response = Timetable.generate()
    return jsonify(response)
