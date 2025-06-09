from app import create_app
from app.routes import ConvertToPDF
import os

# Criar diretórios se não existirem
app_dir = os.path.dirname(os.path.abspath(__file__))
upload_dir = os.path.join(app_dir, 'app', 'uploads')
output_dir = os.path.join(app_dir, 'app', 'output')

os.makedirs(upload_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

app, api = create_app()

# Registrando as rotas
api.add_resource(ConvertToPDF, '/api/v1/convert')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
