FROM python:3.11-slim

# Especificar a versão do Docker
LABEL docker.version="19.03"

# Instala as dependências necessárias para o LibreOffice AppImage
RUN apt-get update && apt-get install -y \
    libfuse2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt .
COPY run.py .
COPY app/ app/

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Cria os diretórios necessários
RUN mkdir -p app/uploads app/output

# Dá permissão de execução ao LibreOffice AppImage
RUN chmod +x app/extra/LibreOffice-fresh.standard-x86_64.AppImage

# Expõe a porta 5000
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
