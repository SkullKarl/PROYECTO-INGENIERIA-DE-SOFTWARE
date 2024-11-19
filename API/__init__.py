# En API/__init__.py

from flask import Flask
from routes.patient_routes import patient_bp
from routes.specialist_routes import specialist_bp
from routes.admin_routes import admin_bp
from routes.block_routes import block_bp
from routes.appointment_routes import appointment_bp

from flask_cors import CORS

def create_app(config_object=None):
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para toda la API
    
    if config_object:
        app.config.from_object(config_object)
    
    # Registrar los Blueprints con prefijos específicos
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(specialist_bp, url_prefix='/specialist')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(block_bp, url_prefix='/blocks')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')

    return app