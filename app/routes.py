from flask import request, send_file, jsonify
from flask_restful import Resource
import os
import subprocess
import base64
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output'))
LIBREOFFICE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extra', 'LibreOffice-fresh.standard-x86_64.AppImage')
ALLOWED_EXTENSIONS = {'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_directories():
    """Limpa os diretórios de upload e output antes de uma nova conversão"""
    try:
        # Limpa diretório de uploads
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        # Limpa diretório de output
        for filename in os.listdir(OUTPUT_FOLDER):
            file_path = os.path.join(OUTPUT_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Erro ao limpar diretórios: {str(e)}")

class ConvertToPDF(Resource):
    def post(self):
        # Limpa os diretórios antes de iniciar uma nova conversão
        cleanup_directories()

        # Garante que os diretórios existem
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        if 'file' not in request.files:
            return {'error': 'Nenhum arquivo enviado'}, 400
        
        file = request.files['file']
        output_type = request.form.get('output_type', 'url')
        
        if file.filename == '':
            return {'error': 'Nenhum arquivo selecionado'}, 400
            
        if not allowed_file(file.filename):
            return {'error': 'Tipo de arquivo não permitido'}, 400
            
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = f"{os.path.splitext(filename)[0]}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Salva o arquivo
        file.save(input_path)
        
        try:
            # Converte para PDF usando LibreOffice AppImage
            process = subprocess.Popen([
                LIBREOFFICE_PATH,
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                OUTPUT_FOLDER,
                input_path
            ])
            process.wait()
            
            if output_type == 'download':
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=output_filename
                )
            
            elif output_type == 'base64':
                with open(output_path, 'rb') as pdf_file:
                    encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
                return {
                    'base64': encoded_pdf,
                    'filename': output_filename,
                    'message': 'Arquivo convertido com sucesso'
                }
                
        except Exception as e:
            return {'error': str(e)}, 500
        
        finally:
            # Limpa o arquivo de upload
            if os.path.exists(input_path):
                os.remove(input_path)
