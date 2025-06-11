# FlaskApp - Conversor de DOC/DOCX para PDF

Este projeto é uma API Flask para converter arquivos `.doc` e `.docx` em PDF, utilizando o LibreOffice AppImage em ambiente Docker.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- (Opcional) [Docker Compose](https://docs.docker.com/compose/) instalado

## Estrutura do Projeto

```
flaskapp/
├── app/
│   ├── routes.py
│   ├── uploads/
│   ├── output/
│   └── extra/
│       └── LibreOffice-fresh.standard-x86_64.AppImage
├── requirements.txt
├── run.py
└── Dockerfile
```

## Como usar

### 1. Coloque o AppImage do LibreOffice

Baixe o arquivo `LibreOffice-fresh.standard-x86_64.AppImage` e coloque em `app/extra/`.

### 2. Build da imagem Docker

```sh
docker build -t flaskapp .
```

### 3. Execute o container

```sh
docker run --rm -p 5000:5000 flaskapp
```

> **Se usar AppImage e der erro de FUSE, rode com:**
> 
> ```sh
> docker run --rm --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined -p 5000:5000 flaskapp
> ```

### 4. Faça requisições para a API

- **Endpoint:** `POST /convert`
- **Form-data:**
  - `file`: arquivo `.doc` ou `.docx`
  - `output_type`: `download` ou `base64` (opcional, padrão: `url`)

#### Exemplo usando `curl`:

```sh
curl -F "file=@seuarquivo.docx" -F "output_type=base64" http://localhost:5000/convert
```

## Observações

- Os arquivos enviados são salvos em `/app/uploads` e os PDFs gerados em `/app/output` dentro do container.
- O diretório de saída é limpo a cada nova conversão.
- O retorno pode ser o arquivo para download ou o PDF em base64.

## Possíveis erros

- **FUSE/AppImage:** Se houver erro ao montar o AppImage, rode o container com permissões extras (veja acima).
- **Dependências:** O Dockerfile já instala as bibliotecas necessárias para o LibreOffice funcionar.

## Licença

MIT