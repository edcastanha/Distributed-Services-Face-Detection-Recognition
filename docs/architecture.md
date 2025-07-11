# Arquitetura do Sistema

O sistema é projetado com uma arquitetura de microsserviços distribuídos, orquestrados com Docker Compose.

- **Servidor Django (`secedu-api`):** Fornece a API REST principal para administração do sistema, gerenciamento de câmeras, cadastros e visualização de dados. Também atua como o ponto de entrada para agendamento de tarefas Celery.

- **Servidor Flask (`secedu-face`):** Uma API dedicada e otimizada para operações de reconhecimento facial de alta performance, utilizando a biblioteca DeepFace.

- **Celery Workers & Beat:**
  - `secedu-beat-scheduler`: Agenda tarefas periódicas.
  - `secedu-tasks-workers`: Executa tarefas assíncronas definidas no Django.

- **Jobs de Processamento de Rosto (`server-jobs-faces`):** Consumidores RabbitMQ independentes que realizam as etapas do pipeline de reconhecimento facial (extração, embedding, análise) de forma assíncrona e escalável.

- **Broker e Filas (`broker-server`):** RabbitMQ gerencia a comunicação entre os serviços, garantindo que as tarefas de processamento de imagem sejam distribuídas de forma confiável.

- **Banco de Dados e Cache:**
  - `postgres-server`: Banco de dados relacional principal.
  - `redis-server`: Utilizado como backend de resultados para o Celery e para caching.

- **Nginx (`secedu-nginx`):** Atua como um proxy reverso para a aplicação Django, servindo arquivos estáticos e direcionando o tráfego.
