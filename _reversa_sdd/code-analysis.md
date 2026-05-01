# Análise de Código: Distributed-Services-Face-Detection-Recognition

A análise de código foi realizada nos seguintes módulos, mapeando lógicas e algoritmos principais do sistema legado:

## 1. Módulo `server-flask-api`
Este módulo expõe uma API robusta de processamento facial construída em Flask.
**Algoritmos principais**:
- **Tratamento e recortes via Mediapipe**: O endpoint `/embedding` implementa lógica manual para recortar o contorno oval do rosto (`FACEMESH_FACE_OVAL`) e criar uma máscara em fundo preto, evitando ruídos de fundo antes de enviar ao `deepface`.
- **Roteamento de Análise Demográfica**: Usa o deepface via wrapper no arquivo `service.py` para as métricas (`age`, `gender`, `emotion`, `race`).
- **Validações**: Todas as chamadas inspecionam extensões de imagens permitidas (jpg, jpeg, png).

## 2. Módulo `server-jobs-faces`
Opera em modo pipeline de mensageria assíncrona, orquestrando fluxos em RabbitMQ.
**Algoritmos principais**:
- **Discovery de arquivos (FTP)**: `start_producer_path` caminha na pasta `ftp/`, extraindo padrões regex `AAAA-MM-DD` de data no nível 3 do diretório, impedindo duplicidade através de um hashset temporário na memória.
- **Publishing de Mensagens**: Transforma metadata das capturas em JSON e propaga para a exchange `secedu` com routing key `path`.

## 3. Módulo `server-django` e `server-celery-worker`
Estes módulos representam o Core de backend relacional e administração. 
Eles agem como orquestradores de dados de longo prazo (persistência) e delegação de tarefas agendadas.

---
**Nível de Confiança da Análise**: 🟢 INFERIDO e CONFIRMADO com base nas leituras dos entrypoints principais (`main.py`, `routes.py`).
