# Máquinas de Estado do Sistema

A máquina de estado principal orbita as Imagens (Frames de FTP) desde que entram no ecossistema até serem analisadas/embutidas (Embeddings) pelo sistema distribuído.

## Entidade: Imagem de Captura / CaptureMessage

```mermaid
stateDiagram-v2
    [*] --> DepositadaNoFTP: Câmera ou Processo FTP Salva
    DepositadaNoFTP --> MapeadaNoRabbitMQ: Lida pelo start_producer_path
    MapeadaNoRabbitMQ --> ExtraindoFace: Consumida pelo consumer-extrair-faces
    ExtraindoFace --> AnalisandoDemografias: Enviada p/ service.analyze (Opcional)
    ExtraindoFace --> CalculandoEmbedding: Enviada p/ service.represent
    AnalisandoDemografias --> SalvaNoBanco: Dados Estruturados em DB (Celery/Django)
    CalculandoEmbedding --> SalvaNoBanco: Embedding Registrado no BD
    SalvaNoBanco --> [*]
    
    ExtraindoFace --> Rejeitada: Rosto Não Encontrado (enforce_detection=True)
    Rejeitada --> [*]
```
