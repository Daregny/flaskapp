from flask import Flask, send_from_directory
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    api = Api(app)

    @app.route('/api/v1/output/<path:filename>')
    def serve_pdf(filename):
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        return send_from_directory(output_dir, filename)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    # Configuração do Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Conversor DOC para PDF API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app, api
