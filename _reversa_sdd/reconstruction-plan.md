# Reconstruction Plan — Distributed Services Face Detection Recognition

**Stack:** Python, Flask, Django, Celery, RabbitMQ, DeepFace
**Gerado em:** 2026-05-01
**Status:** 9 tarefas | 0 concluídas | 9 pendentes

---

## Alertas de pré-voo

Nenhum gap crítico identificado. Pode iniciar com segurança.

---

## Tarefas

### Tarefa 01 — Schema do Banco de Dados
**Status:** pending
**Lê:** `_reversa_sdd/erd-complete.md`, `_reversa_sdd/data-dictionary.md`
**Constrói:** migrations, schema, modelos ORM (conforme stack detectada)
**Pronto quando:** Todas as tabelas do ERD existem com tipos, constraints e foreign keys corretos

---

### Tarefa 02 — Entidades de Domínio
**Status:** pending
**Lê:** `_reversa_sdd/domain.md`, `_reversa_sdd/data-dictionary.md`
**Constrói:** entidades, value objects, validações de domínio
**Pronto quando:** Todas as entidades implementadas com as regras de negócio descritas

---

### Tarefa 03 — Máquinas de Estado
**Status:** pending
**Lê:** `_reversa_sdd/state-machines.md`
**Constrói:** implementação dos fluxos de estado de cada entidade
**Pronto quando:** Todos os estados e transições documentados estão implementados

---

### Tarefa 04 — Fluxo FTP Producer (Jobs Faces)
**Status:** done
**Lê:** `_reversa_sdd/sdd/server-jobs-faces.md`, `_reversa_sdd/dependencies.md`, `_reversa_sdd/user-stories/fluxo-captura-face.md`
**Constrói:** `server-jobs-faces/codes_models/main.py`, `server-jobs-faces/publicar.py`
**Pronto quando:** Dado um diretório 'ftp/camera_01/sub/2026-05-01/foto.jpg', Quando o 'start_producer_path' for executado, Então a foto deve ser mapeada, encapsulada em JSON e despachada para a exchange 'secedu'.

---

### Tarefa 05 — DeepFace Flask API
**Status:** pending
**Lê:** `_reversa_sdd/sdd/server-flask-api.md`, `_reversa_sdd/dependencies.md`
**Constrói:** `server-flask-api/app/api/routes.py`, `server-flask-api/app/api/service.py`
**Pronto quando:** Dado um caminho de imagem válida, a API extrai a face com MediaPipe (loop para múltiplas) e gera embeddings corretos.

---

### Tarefa 06 — Celery Worker
**Status:** pending
**Lê:** `_reversa_sdd/sdd/server-celery-worker.md`, `_reversa_sdd/dependencies.md`
**Constrói:** `server-celery-worker/` (Setup do container Celery)
**Pronto quando:** A fila de eventos for consumida do broker sem gerar timeouts.

---

### Tarefa 07 — Administração Web (Django)
**Status:** pending
**Lê:** `_reversa_sdd/sdd/server-django.md`, `_reversa_sdd/dependencies.md`
**Constrói:** `server-django/` (Models e Views)
**Pronto quando:** O administrador logado consegue visualizar registros persistidos.

---

### Tarefa 08 — Camada de API (Contratos)
**Status:** pending
**Lê:** `_reversa_sdd/openapi/server-flask-api.yaml`
**Constrói:** Validações Pydantic/Marshmallow e documentação Swagger UI
**Pronto quando:** Todos os endpoints respondem rigorosamente aos contratos.

---

### Tarefa 09 — Integração de Fluxos de Usuário
**Status:** pending
**Lê:** `_reversa_sdd/user-stories/fluxo-analise-demografica.md`
**Constrói:** Testes end-to-end simulando a jornada real
**Pronto quando:** Todos os critérios de aceitação das user stories e falhas controladas estão sendo respeitados.
