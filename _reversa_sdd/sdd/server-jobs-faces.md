# Jobs Faces Producer & Consumer

## Visão Geral
Este componente orquestra a lógica de filas (RabbitMQ). Ele varre pastas mapeadas (FTP) em busca de novos frames gerados por câmeras e enfileira essas imagens para serem consumidas pelos scripts locais de extração e análise.

## Responsabilidades
- **Producer:** Descobrir ativamente novas fotos em subdiretórios `AAAA-MM-DD` de cada câmera na pasta local/FTP.
- **Publisher:** Montar metadados das fotos (data, nome_equipamento, path) e publicar na fila (Exchange `secedu`, routing key `path`).
- **Consumer (Opcional):** Arquivos como `consumer-extrair-faces.py` escutam as filas para disparar a API ou processar com a biblioteca embedada.

## Interface
- **Entrada:** Sistema de arquivos (File System Polling) montado em `ftp/`.
- **Saída:** Publicação em rede AMQP (RabbitMQ) usando a lib `pika`.

## Regras de Negócio
- Apenas diretórios no nível exato (depth) e matching a Regex de data (`\d{4}-\d{2}-\d{2}`) são processados. 🟢
- Evitar duplicação: existe um Set (`processed_dates`) em memória que impede submissão repetida da mesma data em uma execução (ou requer limpeza diária). 🟢

## Fluxo Principal
1. O cron/script inicia `start_producer_path()`.
2. Acessa o diretório raiz configurado `FTP_PATH`.
3. Percorre (os.walk) e identifica paths com 4 componentes.
4. Verifica se a `date_capture` já está no HashSet.
5. Gera o JSON payload (data_captura, nome_equipamento, path, etc).
6. Usa a classe `Publisher` (`publicar.py`) para jogar no RabbitMQ.
7. Marca a data como processada em memória.

## Fluxos Alternativos
- **Data já processada:** Registra no logger e ignora (`continue`/`break`).
- **Broker (RabbitMQ) Offline:** Lança `pika.exceptions.AMQPConnectionError`, loga o erro em `loggingMe.py` e interrompe o envio daquele item temporariamente.

## Dependências
- **RabbitMQ:** Necessita da conexão TCP 5672 para escoar as mensagens.
- **File System:** Permissões de leitura no volume mapeado.

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Evitar parsing exaustivo através do short-circuit em `processed_dates`. | `main.py:31` | 🟢 |
| Resiliência | Tratamento do AMQPConnectionError. | `main.py:53` | 🟢 |

> Inferido a partir do código. Validar com equipe de operações.

## Critérios de Aceitação

```gherkin
Dado um diretório "ftp/camera_01/sub/2026-05-01/foto.jpg"
Quando o "start_producer_path" for executado
Então a foto deve ser mapeada, encapsulada em JSON e despachada para a exchange "secedu"

Dado o Broker inativo
Quando o código tentar dar publish
Então deve ocorrer captura do erro "AMQPConnectionError" sem causar crash no processo inteiro
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| `start_producer_path` e File Polling | Must | Sem isso, não entram novos dados no pipeline de IA |
| Bloqueio de duplicatas (`processed_dates`) | Should | Essencial para evitar DDoS interno no RabbitMQ |

> Prioridade inferida por frequência de chamada e posição na cadeia de dependências.

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server-jobs-faces/codes_models/main.py` | `start_producer_path()` | 🟢 |
| `server-jobs-faces/publicar.py` | `Publisher` | 🟢 |

## Cenários de Borda
- **Prevenção de Vazamento de Memória (`processed_dates`)**: O HashSet em memória deve realizar um flush/limpeza automática diariamente ou ser migrado para integração com a camada do Redis, eliminando a ameaça de OOM (Out of Memory) em jornadas 24/7. 🟢
