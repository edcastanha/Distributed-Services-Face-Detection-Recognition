# Processador Celery (Workers)

## Visão Geral
Este componente é a ponte asíncrona conectada ao Django e RabbitMQ, responsável por atuar na camada pesada do negócio, registrando falhas, gerando metadados consolidados no banco ou escalonando pipelines.

## Responsabilidades
- Ler tarefas da fila assíncrona alocadas pelo ecossistema Django.
- Executar processamentos que não poderiam ser feitos durante o request/response síncrono.
- Persistir as análises processadas no DB.

## Interface
- **Entrada:** Tasks Python enfileiradas via broker.
- **Saída:** Mudanças de estado no Database Relacional ou logs no console.

## Regras de Negócio
- Apenas tarefas pré-cadastradas (`@task` ou `@shared_task`) são reconhecidas. 🟡

## Fluxo Principal
1. O processo Worker Celery inicia atrelado ao `docker-compose.yaml` local.
2. Fica escutando por tarefas registradas no broker (RabbitMQ/Redis).
3. Ao receber, executa as funções declaradas sem bloquear a interface principal.
4. Salva o resultado final com status (SUCESSO/FALHA).

## Fluxos Alternativos
- **Task Falha:** Worker fará retry automático se configurado, ou lançará alerta nos logs unificados do Docker.

## Dependências
- **Celery / RabbitMQ / Redis** — Framework e filas.
- **Banco de Dados (Django ORM)** — Para armazenar estados finais de tarefas pesadas.

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Escalabilidade | Celery permite spawnar "n" workers dependendo de recursos da máquina host | Conhecimento padrão do framework Celery | 🟡 |

> Inferido a partir do código. Validar com equipe de operações.

## Critérios de Aceitação

```gherkin
Dado uma fila de eventos de captura preenchida
Quando o Worker Celery for acionado
Então a tarefa deve ser consumida do broker sem repassar erros de timeout para os WebClients.
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Celery Workers Running | Must | Caso caiam, o Django vai acumular tarefas mortas no broker. |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server-celery-worker/` | Dockerfile e Configurações | 🟡 |

## Cenários de Borda
- **Worker Crash por OOM (Out of Memory):** Processar matrizes gigantes de imagens pode estourar a RAM do worker; ele deve reiniciar sozinho. 🟡
