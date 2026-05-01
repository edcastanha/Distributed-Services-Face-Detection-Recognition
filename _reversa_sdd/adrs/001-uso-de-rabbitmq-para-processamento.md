# ADR-001: Uso de RabbitMQ para Processamento Assíncrono de Imagens

**Status:** Aceito (Retroativo)  
**Data:** 2026-05-01 (Data da Engenharia Reversa)

## Contexto e Problema
A extração de faces em vídeos/fotos é altamente intensiva na GPU/CPU. Processar cada imagem do FTP de forma síncrona levaria ao estrangulamento imediato do script e perda de progresso durante reinícios abruptos.

## Decisão
Foi adotado um padrão de Fila de Mensagens (`RabbitMQ`) usando a biblioteca `pika` (`server-jobs-faces/codes_models/main.py`), com exchange chamado `secedu` e routing_key `path`.

## Alternativas Consideradas
1. **Cronjob sequencial (sem filas)**: Foi descartado pois travaria a thread principal processando as detecções sincronicamente.
2. **Kafka**: Descartado por ser muito pesado e complexo para os volumes exigidos que requeriam apenas roteamento simples por worker.

## Consequências
- **Positivo:** Escalonamento horizontal; é possível rodar dezenas de instâncias Docker consumindo faces em paralelo.
- **Negativo:** Adiciona complexidade infraestrutural; o RabbitMQ e seu servidor Erlang se tornam um ponto único de falha para o tracking.
