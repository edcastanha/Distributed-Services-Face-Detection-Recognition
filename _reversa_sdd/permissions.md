# Matriz de Permissões (RBAC)

Devido à arquitetura do `server-django`, assume-se o padrão nativo de grupos de permissões de painel de controle (Admin UI).
A API Flask (`server-flask-api`) funciona em regime headless de Microserviço, servindo exclusivamente outros sistemas.

## Funções Atuantes

| Papel (Role) | Descrição |
|--------------|-----------|
| **Admin Geral (SuperUser Django)** | Pode manipular regras de câmera, configurações de rabbitmq, e visualizar o banco de dados principal de embeddings. |
| **Worker (RabbitMQ/Celery)** | Consumidor interno do sistema de rede de confiança que insere registros via ORM (Celery) ou endpoints da API. |

## Matriz (Admin do Django)

| Recurso / Módulo | Ver | Criar | Editar | Excluir |
|------------------|-----|-------|--------|---------|
| Configuração de FTP | ✅ | ✅ | ✅ | ✅ |
| Modelos/Embeddings Salvos | ✅ | ❌ (Automático) | ❌ | ✅ |
| Logs de Processamento | ✅ | ❌ | ❌ | ❌ |
