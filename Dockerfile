FROM python:3.11

# Especificar a versão do Docker
LABEL docker.version="19.03"

# Instala as dependências necessárias para o LibreOffice AppImage
RUN apt-get update && apt-get install -y \
    libfuse2 \
    libnss3 \
    libdbus-1-3 \
    libcups2 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt .
COPY run.py .
COPY app/ app/
# Copia o AppImage já com permissão de execução
COPY app/extra/LibreOffice-fresh.standard-x86_64.AppImage app/extra/
RUN chmod +x app/extra/LibreOffice-fresh.standard-x86_64.AppImage

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Cria os diretórios necessários dentro de /app/app/
RUN mkdir -p output uploads

# Expõe a porta 5000
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
