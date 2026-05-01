```mermaid
graph TD
    A[Django View / Job] -->|delay() task| B(RabbitMQ / Broker)
    B --> C[Celery Worker Consume]
    C --> D{Executa Tarefa Assíncrona}
    D --> E[Processamento de Dados e Modelos]
    E --> F[Salva Resultado no Banco / Cache]
```
