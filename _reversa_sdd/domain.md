# Domínio do Sistema: SecEdu Face Detection & Recognition

## Glossário de Negócio

| Termo | Definição |
|-------|-----------|
| **DeepFace** | Biblioteca subjacente de reconhecimento e detecção facial em Python, abstraída pela API Flask. |
| **Embeddings** | Representação vetorial matemática de rostos usada para cálculos de distâncias (Cosine) e verificação de similaridade. |
| **Landmarks (Mediapipe)** | Pontos de referência extraídos do rosto (ex: contorno facial oval) para isolar faces do background e melhorar a precisão no processo de validação. |
| **CaptureMessage** | Representa o path FTP de uma imagem no RabbitMQ pronta para extração facial. |

## Regras de Negócio Implícitas (Detetive)

1. **Padrão de Armazenamento de Arquivos em FTP**:
   - As imagens depositadas nas pastas FTP devem obrigatoriamente usar a organização que contemple `YYYY-MM-DD` no quarto nível (`/path/to/device/YYYY-MM-DD`).
   - Se esta estrutura de diretórios for violada, o Producer as ignorará na leitura para o RabbitMQ.

2. **Alinhamento e Limpeza (API)**:
   - Os rostos devem sofrer extração/mascaramento via MediaPipe para remover fundos (background) no cálculo do embedding antes de acionar o pipeline do deepface, evitando "falsos positivos" de identificação.

3. **Arquitetura Desacoplada e Resiliência**:
   - O processo de detecção em tempo real e de extração contínua (jobs faces) é feito usando mensageria RabbitMQ para enfileirar as tarefas. Caso o sistema caia, as mensagens garantem tolerância à falha e processamento posterior.
