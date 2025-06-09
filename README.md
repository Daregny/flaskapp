# Conversor DOC para PDF API

API REST desenvolvida com Flask para converter arquivos DOC/DOCX para PDF utilizando LibreOffice.

## Descrição

Esta API permite converter arquivos do Microsoft Word (DOC/DOCX) para PDF utilizando o LibreOffice em modo headless. A API oferece duas opções de retorno:
- Download direto do arquivo PDF
- Retorno do arquivo em formato Base64

## Requisitos

- Docker 19.03 ou superior
- Docker Compose

## Estrutura do Projeto

```
.
├── app/
│   ├── extra/              # Contém o LibreOffice AppImage
│   ├── output/             # Diretório para arquivos PDF convertidos
│   ├── uploads/            # Diretório para arquivos DOC/DOCX temporários
│   ├── static/            
│   │   └── swagger.json    # Documentação da API
│   ├── __init__.py        # Configuração do Flask
│   └── routes.py          # Rotas e lógica da API
├── docker-compose.yml      # Configuração do Docker Compose
├── Dockerfile             # Configuração do container
├── requirements.txt       # Dependências Python
└── run.py                # Arquivo principal para execução
```

## Como Executar

1. Clone o repositório:
```bash
git clone <repositório>
cd flaskapp
```

2. Coloque o arquivo LibreOffice AppImage na pasta `app/extra/`:
```bash
# Certifique-se que o arquivo está nomeado como:
LibreOffice-fresh.standard-x86_64.AppImage
```

3. Construa e inicie o container:
```bash
docker-compose up --build
```

4. A API estará disponível em:
```
http://localhost:5000
```

## Documentação da API

A documentação Swagger UI está disponível em:
```
http://localhost:5000/api/docs
```

### Endpoint

`POST /api/v1/convert`

#### Parâmetros

- `file`: Arquivo DOC/DOCX para converter (required)
- `output_type`: Tipo de saída desejado (required)
  - `download`: Download direto do PDF
  - `base64`: Retorno do PDF em base64

## Volumes Docker

O projeto utiliza três volumes Docker:
- `./app/uploads`: Para arquivos temporários
- `./app/output`: Para arquivos convertidos
- `./app/extra`: Para o LibreOffice AppImage

## Ambiente de Desenvolvimento

Para desenvolvimento local sem Docker:

1. Crie um ambiente virtual:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# ou
env\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python run.py
```

## Observações

- Os diretórios de upload e output são limpos automaticamente antes de cada nova conversão
- O LibreOffice é executado em modo headless para otimizar o uso de recursos
- A API utiliza CORS para permitir requisições de diferentes origens