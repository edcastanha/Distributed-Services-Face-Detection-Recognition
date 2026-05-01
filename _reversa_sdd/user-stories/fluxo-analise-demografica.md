# User Story: Fluxo de Análise Demográfica (API)

**Como um** serviço Worker de Backend
**Eu quero** submeter um path de imagem capturada para a API de DeepFace
**Para que** o sistema gere os embeddings e extraia informações demográficas (Idade, Gênero, Raça e Emoção) da pessoa flagrada.

## Critérios de Aceite
- **Cenário 1: Caminho Válido com Rosto (Happy Path)**
  - **Dado** que o path passado aponte para um `.jpg` ou `.png` legítimo com um rosto bem definido
  - **Quando** o POST for disparado para a rota `/analyze`
  - **Então** o JSON de saída deve conter os vetores de probabilidade demográfica corretos e status 200.

- **Cenário 2: Enforce Detection (Nenhum Rosto)**
  - **Dado** que o path passado contém uma foto do chão (sem humanos) e `enforce_detection = True`
  - **Quando** o POST bater no `/analyze`
  - **Então** o DeepFace/Mediapipe deve retornar erro controlado em JSON notificando "Face could not be detected" (ou derivado) em vez de corromper o serviço.

- **Cenário 3: Extensão Recusada**
  - **Dado** uma imagem falsa com final `.gif`
  - **Quando** bater na rota `/analyze`
  - **Então** a API deve falhar na validação primária e retornar a string `"é necessário passar a entrada imagem valido com extensão .jpg, .png ou .jpeg"`.

## Notas Técnicas
- **Origem:** Extraído de `routes.py:analyze()`.
- O endpoint processa as keys defaults `actions = ["age", "gender", "emotion", "race"]`.
