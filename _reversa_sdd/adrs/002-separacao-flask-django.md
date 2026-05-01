# ADR-002: Separação Arquitetural do Microserviço Flask e Django Admin

**Status:** Aceito (Retroativo)  
**Data:** 2026-05-01 (Data da Engenharia Reversa)

## Contexto e Problema
O DeepFace possui grandes pesos na memória (modelos TensorFlow, MediaPipe) e consome recursos altos. Misturar o painel de administração (Frontend UI, Banco de Dados) no mesmo ecossistema (e mesmo worker) da análise de IA poderia causar timeouts e instabilidades constantes para usuários do sistema administrativo.

## Decisão
A arquitetura foi desmembrada em dois monólitos especialistas (SOA/Microsserviços):
- `server-django`: Focado 100% no CRUD de administração, banco e interface HTML/CSS, sem carregar os pesados scripts do TensorFlow.
- `server-flask-api`: Focado 100% em processamento neural de imagens, atuando como um endpoint "stateless" chamado sob demanda, sem interfaces gráficas.

## Alternativas Consideradas
1. **Django Unificado com Tarefas Celery para o DeepFace**: Foi evitado pois inflaria muito o contêiner principal da interface web.

## Consequências
- **Positivo:** A interface Web e o Banco de Dados operam rápido pois estão isolados do gargalo de processamento da IA.
- **Negativo:** Requer a gestão de dois serviços na orquestração Docker (`docker-compose.yaml`).
