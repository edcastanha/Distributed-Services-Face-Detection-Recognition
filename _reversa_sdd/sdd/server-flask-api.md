# Microserviço Flask API (DeepFace API)

## Visão Geral
Este componente é a API REST central (stateless) construída em Flask, focada em fornecer endpoints para a análise de imagens, recortes de face e inferência demográfica ou verificação via DeepFace e MediaPipe.

## Responsabilidades
- Receber payloads HTTP POST com caminhos para imagens.
- Fazer a extração isolada dos rostos (usando MediaPipe para recortes complexos de contorno `FACEMESH_FACE_OVAL`).
- Chamar internamente as bibliotecas de IA (`DeepFace.analyze`, `DeepFace.verify`, `DeepFace.represent`).
- Retornar o resultado do processamento estruturado em JSON para os clients internos (como Celery).

## Interface
**Principais Endpoints REST:**
- `POST /analyze`: Recebe `{"img_path": "...", "actions": ["age", ...]}`. Retorna demografias.
- `POST /verify`: Recebe `{"img1_path": "...", "img2_path": "..."}`. Retorna `{"verified": true/false}`.
- `POST /embedding`: Recebe `{"img": "..."}`. Retorna o vetor da face.

## Regras de Negócio
- Apenas imagens com extensão `.jpg`, `.jpeg` ou `.png` são permitidas. 🟢
- Caso a imagem não possua rosto ou não seja detectada, a chave `enforce_detection=True` fará a API retornar falha imediata, evitando processar lixo. 🟢
- MediaPipe atua cortando um polígono convexo em formato oval apenas sob a face; o restante da foto é zerado (preto), melhorando o embedding. 🟢

## Fluxo Principal
1. O endpoint `/embedding` ou `/analyze` recebe a requisição com JSON contendo `img_path`.
2. Há validação primária de formato.
3. Se roteado para `/embedding`, o opencv (`cv2`) carrega a imagem.
4. O `mp_face_mesh` traça pontos no rosto, criando máscara.
5. O recorte é passado ao wrapper do DeepFace.
6. A API retorna os atributos detectados na resposta JSON.

## Fluxos Alternativos
- **Caminho ausente ou não suportado:** A API não quebra; retorna JSON de erro `{"message": "é necessário passar a entrada img_path com extensão..."}`.
- **Falha no DeepFace (excepções):** São capturadas no bloco try/except e retornadas como `{"error": "<msg>"}`.

## Dependências
- **DeepFace** — Engine base neural.
- **MediaPipe** — Marcações e Landmarks.
- **Celery Workers** — Consome estes endpoints.

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Validação estrita de payload json de entrada HTTP. | `routes.py:32` | 🟢 |
| Escalabilidade | Arquitetura de microsserviço stateless (não tem sessão nem DB embutido). | `routes.py` inteiro | 🟡 |

> Inferido a partir do código. Validar com equipe de operações.

## Critérios de Aceitação

```gherkin
Dado um caminho de imagem .jpg válida com um rosto humano
Quando enviamos uma requisição POST para /analyze
Então a API deve retornar sucesso (200 OK) com as chaves "age", "gender", "emotion" e "race"

Dado um caminho inválido ou arquivo .txt em /embedding
Quando fazemos um POST
Então a API deve retornar "é necessário passar a entrada img_path com extensão..."
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Endpoints /analyze e /embedding | Must | Caminho crítico — chamado em todo fluxo de reconhecimento |
| Máscara MediaPipe | Should | Importante para extração limpa (redução de falsos positivos) |
| Endpoint /dataset | Could | Rota auxiliar para limpar cache de testes |

> Prioridade inferida por frequência de chamada e posição na cadeia de dependências.

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server-flask-api/app/api/routes.py` | `analyze()`, `verify()`, `embedding()` | 🟢 |
| `server-flask-api/app/api/service.py` | (Wrapper deepface) | 🟡 |

## Cenários de Borda
- **Múltiplos rostos na imagem**: A arquitetura prevê iterar sobre todos os rostos detectados no array `landmarks.landmark`, recortando e processando as extrações paralelamente para garantir que imagens com multidões não percam as pessoas adicionais. 🟢
