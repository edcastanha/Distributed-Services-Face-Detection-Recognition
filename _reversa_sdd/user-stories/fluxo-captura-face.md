# User Story: Fluxo de Captura de Face

**Como um** sistema de processamento de filas (Worker/Producer)
**Eu quero** rastrear automaticamente novas imagens na rede (FTP)
**Para que** eu possa enviar as capturas para o microserviço e gerar modelos neurais das pessoas flagradas.

## Critérios de Aceite
- **Cenário 1: Pasta com estrutura de data válida**
  - **Dado** que há uma imagem fotográfica na pasta `/ftp/catraca_01/sub/2026-05-01/foto.jpg`
  - **Quando** o `start_producer_path` rodar sua rotina de discover
  - **Então** ele deve extrair a data "2026-05-01"
  - **E** deve empacotar no payload e subir na queue "secedu" do RabbitMQ.
  - **E** a data deve ser marcada como processada em memória para não repetir na mesma run.

- **Cenário 2: Erro na fila AMQP**
  - **Dado** que o RabbitMQ está offline
  - **Quando** o script tentar publicar
  - **Então** o sistema deve fazer fallback no log ("AMQPConnectionError") e não travar o for-loop inteiro.

## Notas Técnicas
- **Origem:** Reversamente extraído do script `main.py` de `server-jobs-faces`.
- A identificação ocorre baseada num regex rígido: `\d{4}-\d{2}-\d{2}`. Qualquer nomeação fora disso será descartada sumariamente pela árvore `os.walk`.
