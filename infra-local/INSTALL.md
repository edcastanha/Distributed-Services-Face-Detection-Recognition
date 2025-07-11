# Guia de Instalação Local com Docker Compose

Este guia fornece as instruções para configurar e executar o ambiente de desenvolvimento localmente usando Docker e Docker Compose.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em sua máquina:

1.  **Docker Engine:** [Instruções de instalação](https://docs.docker.com/engine/install/)
2.  **Docker Compose:** [Instruções de instalação](https://docs.docker.com/compose/install/)
3.  **NVIDIA Driver:** É necessário ter um driver NVIDIA compatível instalado.
4.  **NVIDIA Container Toolkit:** Essencial para habilitar o suporte a GPU nos contêineres Docker.
    - [Instruções de instalação](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/Distributed-Services-Face-Detection-Recognition.git
    cd Distributed-Services-Face-Detection-Recognition/infra-local
    ```

2.  **Crie o arquivo de variáveis de ambiente:**
    O arquivo `docker-compose.yaml` utiliza um arquivo `.env` para configurar os serviços. Você pode criar este arquivo a partir do exemplo `env.txt`.
    ```bash
    cp env.txt .env
    ```
    *Nota: Revise o arquivo `.env` e ajuste as variáveis conforme necessário para o seu ambiente.*

3.  **Crie os diretórios de volumes:**
    O Docker Compose está configurado para usar volumes locais (bind mounts). Crie os diretórios necessários na pasta `infra-local` se eles não existirem:
    ```bash
    mkdir -p volumes/{postgres,rabbitmq,redis,weights,logs,server_ftp,capturas,dataset,faces-oval,staticfiles}
    ```

## Execução do Ambiente

Com o ambiente configurado, você pode iniciar todos os serviços com um único comando a partir do diretório `infra-local`:

```bash
docker-compose up -d --build
```

Este comando irá construir as imagens (se necessário) e iniciar todos os 12 serviços em segundo plano (`-d`).

## Verificação

Para verificar se o ambiente está funcionando corretamente:

1.  **Liste os contêineres em execução:**
    ```bash
    docker-compose ps
    ```
    Você deve ver todos os serviços com o status `Up` ou `running`.

2.  **Verifique os logs (se necessário):**
    Para ver os logs de um serviço específico (por exemplo, `secedu-api`):
    ```bash
    docker-compose logs -f secedu-api
    ```

3.  **Acesse as Interfaces Web:**
    *   **RabbitMQ Management:** [http://localhost:15672](http://localhost:15672) (usuário: `secedu`, senha: `mudar1234`)
    *   **RedisInsight:** [http://localhost:8001](http://localhost:8001)
    *   **API Django (via Nginx):** [http://localhost:7000](http://localhost:7000)

## Pós-Instalação (Configuração Inicial do Banco de Dados)

Após iniciar os contêineres pela primeira vez, você precisa executar as migrações do Django e, opcionalmente, carregar os dados de exemplo.

Execute os seguintes comandos para entrar no contêiner da API Django e aplicar as configurações:

1.  **Executar as migrações do banco de dados:**
    ```bash
    docker-compose exec secedu-api python manage.py makemigrations --noinput
    docker-compose exec secedu-api python manage.py migrate --noinput
    ```

2.  **Coletar arquivos estáticos:**
    ```bash
    docker-compose exec secedu-api python manage.py collectstatic --noinput
    ```

3.  **(Opcional) Carregar dados de backup:**
    Se você deseja popular o banco de dados com dados de exemplo, execute os comandos de `loaddata` conforme o arquivo `COMANDOS.md`. Exemplo:
    ```bash
    docker-compose exec secedu-api python manage.py loaddata backup-models/cadastros/cadastros.json
    docker-compose exec secedu-api python manage.py loaddata backup-models/cameras/cameras_Cameras.json
    # ... e assim por diante para os outros arquivos.
    ```

Com estes passos, o ambiente de desenvolvimento estará totalmente operacional.
