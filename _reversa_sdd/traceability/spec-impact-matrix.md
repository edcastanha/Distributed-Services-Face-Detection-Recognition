# Spec Impact Matrix

Esta matriz rastreia como as modificações arquiteturais de um Container/Módulo afetam outro.

| Componente Modificado | Componentes Impactados Diretamente | Nível de Risco | Observações |
|-----------------------|------------------------------------|----------------|-------------|
| **DeepFace Models** | `flask_api` | **Alto** | Mudanças nos pesos ou backend (ex: de opencv para retinaface) podem mudar a dimensão dos embeddings, invalidando o banco de dados atual. |
| **Padrão de Pastas FTP** | `server-jobs-faces` | **Alto** | Se as câmeras mudarem de `YYYY-MM-DD` para outro padrão, o Producer Python `start_producer_path` irá parar de ler. |
| **RabbitMQ Exchange** | `server-celery-worker` | **Médio** | Mudanças nos routing_keys ou estrutura do JSON `CaptureMessage` quebram a fila e desativam Celery. |
| **Django UI / Models** | Banco de Dados Relacional | **Médio** | Alterações geram migrations que exigem update unificado nos workers que salvam no banco. |
