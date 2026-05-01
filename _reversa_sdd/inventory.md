# Inventário do Projeto: Distributed-Services-Face-Detection-Recognition

## Estrutura de Pastas e Módulos Principais

A estrutura principal do projeto é dividida nos seguintes módulos:

- **server-django/**: Interface e painel de administração (Django).
- **server-flask-api/**: API baseada em Flask para detecção e reconhecimento facial usando DeepFace.
- **server-jobs-faces/**: Workers/Consumers para processamento de faces em background.
- **server-celery-worker/**: Workers baseados em Celery.
- **infra-local/**: Configurações de infraestrutura local via Docker Compose.

*A pasta `./estudos` foi intencionalmente ignorada da análise.*

## Linguagens e Tecnologias

- **Python** (~173 arquivos) é a linguagem predominante em todo o backend.
- **JavaScript/TypeScript** (~174 arquivos js e 90 ts) está presente, mas focado em vendors (Chart.js, TinyMCE) dentro do painel Django.
- **HTML/CSS/JSON** compõem a parte de frontend do Django.

## Frameworks Identificados

- Django (server-django)
- Flask (server-flask-api)
- Celery (server-celery-worker)
- DeepFace (server-flask-api, server-jobs-faces)

## Pontos de Entrada

- Dockerfiles: Presentes em cada módulo (`server-django`, `server-flask-api`, `server-jobs-faces`, `server-celery-worker`).
- Docker Compose: `infra-local/docker-compose.yaml`, `server-celery-worker/docker-compose.yaml`.
- Scripts de inicialização (`main.py`, `setup.py`) presentes nos módulos correspondentes.
