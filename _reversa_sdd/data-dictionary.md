# Dicionário de Dados Completo

Este dicionário foi extraído a partir das estruturas circulantes (mensageria e requests) do sistema.

## Entidade: `CaptureMessage` (Mensageria RabbitMQ)
Mensagem disparada pelo `server-jobs-faces`.

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `data_captura` | string | Sim | Data extraída da pasta no formato `YYYY-MM-DD`. |
| `nome_equipamento` | string | Sim | Nome da câmera/dispositivo no diretório. |
| `caminho_do_arquivo` | string | Sim | Path relativo da imagem no sistema. |
| `data_processamento` | string (ISO8601) | Sim | Timestamp de quando a mensagem foi lida pelo produtor. |

## Request: `AnalyzeRequest` (API Flask)
Payload aceito pelas rotas REST.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `img_path` | string | Sim | - | Path da imagem. |
| `detector_backend` | string | Não | `opencv` | Backend usado para detecção da face. |
| `enforce_detection` | boolean | Não | `True` | Se True, falha caso rosto não seja encontrado. |
| `align` | boolean | Não | `True` | Se True, faz o alinhamento dos olhos do rosto. |
| `actions` | array[string] | Não | `["age", "gender", "emotion", "race"]` | Análises demográficas desejadas. |
