# En API/__init__.py

from flask import Flask
from API.routes.patient_routes import patient_bp
from API.routes.specialist_routes import specialist_bp
from API.routes.admin_routes import admin_bp

def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    
    # Registrar los Blueprints con prefijos específicos
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(specialist_bp, url_prefix='/specialist')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app