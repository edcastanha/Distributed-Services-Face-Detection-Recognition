# ADR-001: Modelos de Dados (Entidades) do Sistema

| Campo       | Valor                              |
|-------------|------------------------------------|
| **Status**  | Aceito                             |
| **Data**    | 2024-01-01                         |
| **Autores** | Equipe de Desenvolvimento          |

---

## Contexto

O sistema de Detecção e Reconhecimento Facial Distribuído precisa persistir e relacionar diferentes categorias de informação para suportar seu pipeline de processamento. São eles:

- Cadastro de pessoas, escolas e contratos;
- Gerenciamento de câmeras e locais de monitoramento;
- Controle de agendamento e execução de tarefas de captura;
- Armazenamento do pipeline de processamento de imagens e detecção de faces;
- Resultados de reconhecimento facial e análise emocional;
- Registro de frequência escolar.

O Django ORM foi escolhido como camada de abstração do banco de dados (PostgreSQL), e as entidades foram organizadas em três aplicações Django:

- **`cadastros`** – dados de cadastro institucional e de pessoas;
- **`cameras`** – equipamentos, locais, tarefas e pipeline de processamento;
- **`analytical`** – resultados analíticos gerados pelo pipeline de IA.

---

## Decisão

### Modelo Base Abstrato (`baseModel`)

Todas as entidades de domínio herdam de um modelo abstrato comum que fornece rastreabilidade temporal automática:

| Campo              | Tipo            | Descrição                      |
|--------------------|-----------------|--------------------------------|
| `data_cadastro`    | DateTimeField   | Preenchido automaticamente na criação |
| `data_atualizacao` | DateTimeField   | Atualizado automaticamente a cada edição |

---

### App `cadastros` — Entidades de Cadastro

#### `Contratos`
Representa o contrato firmado entre a instituição e o prestador do serviço.

| Campo         | Tipo          | Descrição                              |
|---------------|---------------|----------------------------------------|
| `protocolo`   | CharField(100)| Identificador/número do contrato       |
| `assinado_em` | DateTimeField | Data e hora da assinatura              |
| `responsavel` | CharField(100)| Nome do responsável pelo contrato      |

**Relações:** nenhuma (entidade raiz de domínio institucional).

---

#### `Escolas`
Representa a unidade escolar atendida pelo sistema.

| Campo      | Tipo          | Descrição                                   |
|------------|---------------|---------------------------------------------|
| `nome`     | CharField(100)| Nome da escola                              |
| `contrato` | FK → Contratos| Contrato vigente ao qual a escola pertence  |

**Relações:** N:1 com `Contratos`.

---

#### `Pessoas`
Cadastro central de indivíduos — estudantes, colaboradores e tutores.

| Campo    | Tipo          | Descrição                                               |
|----------|---------------|---------------------------------------------------------|
| `nome`   | CharField(100)| Nome completo                                           |
| `sexo`   | CharField     | `Masculino` / `Feminino` / `Outros`                     |
| `perfil` | CharField     | `Tutor` / `Colaborador` / `Estudante`                   |

**Relações:** referenciada por `Fotos`, `Aluno`, `FrequenciasEscolar` e `FacesVerify`.

---

#### `Turmas`
Agrupa estudantes em turmas vinculadas a uma escola.

| Campo     | Tipo           | Descrição                                                   |
|-----------|----------------|-------------------------------------------------------------|
| `nome`    | CharField(50)  | Nome ou código da turma                                     |
| `periodo` | CharField      | `Morning` / `Afternoon` / `Outros`                          |
| `escola`  | FK → Escolas   | Escola à qual a turma pertence                              |
| `alunos`  | M2M → Pessoas  | Estudantes matriculados (via tabela intermediária `Aluno`)  |
| `ensino`  | CharField      | `Children` (Infantil) / `Elementary School` (Fundamental I) |

**Relações:** N:1 com `Escolas`; M:N com `Pessoas` via `Aluno`.

---

#### `Aluno`
Tabela intermediária do relacionamento M:N entre `Pessoas` e `Turmas`, adicionando a matrícula como atributo próprio.

| Campo      | Tipo          | Descrição               |
|------------|---------------|-------------------------|
| `pessoa`   | FK → Pessoas  | Cadastro do estudante   |
| `turma`    | FK → Turmas   | Turma de matrícula      |
| `matricula`| CharField(10) | Número de matrícula     |

---

#### `Escalas`
Define os blocos de horários de um turno escolar vinculados a um contrato.

| Campo           | Tipo          | Descrição                                                                  |
|-----------------|---------------|----------------------------------------------------------------------------|
| `horario_inicio`| TimeField     | Início do período                                                          |
| `horario_fim`   | TimeField     | Fim do período                                                             |
| `contrato`      | FK → Contratos| Contrato ao qual a escala pertence                                         |
| `itinerario`    | CharField     | Turno: `Morning` / `Afternoon` / `Night`                                   |
| `periodo`       | CharField     | Slot: `Entrada`, `Período 1–9`, `Intervalo`, `Extra`, `Saida` (max_length=15) |

**Relações:** N:1 com `Contratos`; referenciada por `Tarefas`.

---

#### `Fotos`
Armazena as fotos de uma `Pessoa` usadas como dataset de referência para reconhecimento facial. O limite é de **10 fotos por pessoa**.

| Campo    | Tipo          | Descrição                                                  |
|----------|---------------|------------------------------------------------------------|
| `pessoa` | FK → Pessoas  | Dono das fotos                                             |
| `foto`   | ImageField    | Arquivo de imagem, salvo em `dataset/<pessoa_id>/<arquivo>`|

**Comportamentos especiais:**
- `pre_save`: ao substituir uma foto, o arquivo antigo é removido do disco e o dataset da API Flask é regenerado.
- `pre_delete`: ao excluir o registro, o arquivo é removido do disco e o dataset é regenerado.

---

### App `cameras` — Equipamentos e Pipeline de Processamento

#### `NotaFiscal`
Nota fiscal de aquisição de câmeras.

| Campo    | Tipo          | Descrição                    |
|----------|---------------|------------------------------|
| `numero` | CharField(100)| Número da nota fiscal        |
| `data`   | DateTimeField | Data de emissão              |

**Relações:** referenciada por `Cameras`.

---

#### `Cameras`
Representa um equipamento de câmera cadastrado no sistema.

| Campo      | Tipo          | Descrição                                      |
|------------|---------------|------------------------------------------------|
| `nf`       | FK → NotaFiscal| Nota fiscal de aquisição                      |
| `descricao`| CharField(100)| Descrição livre                                |
| `acesso`   | CharField(100)| URL ou endereço IP de acesso ao stream         |
| `modelo`   | CharField(50) | Modelo do equipamento                          |
| `usuario`  | CharField(100)| Credencial de acesso — usuário                 |
| `senha`    | CharField(100)| Credencial de acesso — senha                   |
| `status`   | BooleanField  | `True` = ativa, `False` = inativa              |

**Relações:** N:1 com `NotaFiscal`; referenciada por `Locais`, `Tarefas`, `Processamentos` e `FrequenciasEscolar`.

---

#### `Locais`
Associa uma câmera a um ponto físico dentro de uma escola.

| Campo      | Tipo          | Descrição                          |
|------------|---------------|------------------------------------|
| `ponto`    | FK → Escolas  | Escola onde a câmera está instalada|
| `camera`   | FK → Cameras  | Câmera instalada no local          |
| `nome`     | CharField(100)| Nome do ponto (ex.: "Portaria")    |
| `descricao`| CharField(100)| Descrição adicional                |

---

#### `Tarefas`
Representa uma tarefa agendada de captura — associa uma câmera a uma escala de horários.

| Campo     | Tipo          | Descrição                                             |
|-----------|---------------|-------------------------------------------------------|
| `descricao`| CharField(100)| Descrição da tarefa                                  |
| `escalas` | FK → Escalas  | Escala de horários que dispara a tarefa               |
| `cameras` | FK → Cameras  | Câmera responsável pela captura                       |
| `status`  | CharField     | `Pendente` / `Cancelado` / `Erro` / `Finalizado`      |

---

#### `Processamentos`
Registro de cada lote de imagens/vídeo capturado por uma câmera em uma data e horário específicos.

| Campo    | Tipo           | Descrição                                   |
|----------|----------------|---------------------------------------------|
| `camera` | FK → Cameras   | Câmera origem da captura                    |
| `dia`    | CharField(10)  | Data da captura (`DD/MM/YYYY`)              |
| `horario`| CharField(10)  | Horário da captura (opcional)               |
| `path`   | CharField(250) | Caminho único do arquivo no sistema de arquivos |
| `status` | CharField      | `Criado` / `Processado` / `Error`           |
| `retry`  | IntegerField   | Contador de tentativas de reprocessamento   |

**Relações:** N:1 com `Cameras`; referenciada por `Faces` e `FrequenciasEscolar`.

---

#### `Faces`
Cada registro representa uma face detectada dentro de um `Processamento`.

| Campo              | Tipo          | Descrição                                               |
|--------------------|---------------|---------------------------------------------------------|
| `processamento`    | FK → Processamentos | Lote de onde a face foi extraída                 |
| `path_face`        | CharField(350)| Caminho único do recorte de face no disco               |
| `backend_detector` | CharField(20) | Algoritmo detector utilizado (padrão: `retinaface`)     |
| `auditado`         | BooleanField  | Indica se a face foi revisada manualmente               |
| `status`           | CharField     | `Criado` / `Processado` / `Error`                       |

**Relações:** N:1 com `Processamentos`; referenciada por `ImagensTratadas` e `FacesVerify`.

---

#### `FrequenciasEscolar`
Registra a presença de uma pessoa detectada pelo sistema de reconhecimento facial.

| Campo            | Tipo            | Descrição                                          |
|------------------|-----------------|----------------------------------------------------|
| `pessoa`         | FK → Pessoas    | Pessoa identificada                                |
| `camera`         | FK → Cameras    | Câmera que registrou a presença                    |
| `file_dataset`   | CharField(500)  | Caminho do arquivo de referência no dataset        |
| `caminho_do_face`| CharField(500)  | Caminho do recorte de face que gerou o registro    |
| `processo`       | FK → Processamentos | Lote de processamento associado               |
| `data`           | DateField       | Data do registro de frequência                     |
| `horario`        | TimeField       | Horário do registro de frequência                  |

---

### App `analytical` — Resultados Analíticos

#### `ImagensTratadas`
Controla o estado de pré-processamento (tratamento) de uma face detectada.

| Campo     | Tipo          | Descrição                                         |
|-----------|---------------|---------------------------------------------------|
| `face`    | FK → Faces    | Face detectada a ser tratada                      |
| `auditado`| BooleanField  | Se foi revisada manualmente                       |
| `status`  | BooleanField  | `True` = tratamento concluído                     |

---

#### `FacesVerify`
Armazena o resultado da comparação entre uma face detectada e o dataset de referência.

| Campo     | Tipo          | Descrição                                                          |
|-----------|---------------|--------------------------------------------------------------------|
| `face`    | FK → Faces    | Face detectada submetida à verificação                             |
| `verify`  | BooleanField  | `True` = face reconhecida com sucesso                              |
| `distance`| FloatField    | Distância de similaridade entre os embeddings (quanto menor, mais similar) |
| `auditado`| BooleanField  | Se o resultado foi auditado manualmente                            |
| `pessoa`  | FK → Pessoas  | Pessoa identificada (nulo se não identificada)                     |
| `status`  | CharField     | `0` = Analisada / `1` = Auditada / `2` = Rejeitada                 |

---

#### `FacesPrevisaoEmocional`
Armazena os resultados da análise emocional realizada sobre uma face.

| Campo         | Tipo       | Descrição                                                                    |
|---------------|------------|------------------------------------------------------------------------------|
| `auditado`    | BooleanField| Se foi revisada manualmente                                                 |
| `predominante`| CharField  | Emoção predominante detectada: `angry`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise` |
| `zangado`     | FloatField | Probabilidade de raiva (angry)                                               |
| `repulsa`     | FloatField | Probabilidade de repulsa (disgust)                                           |
| `medo`        | FloatField | Probabilidade de medo (fear)                                                 |
| `feliz`       | FloatField | Probabilidade de felicidade (happy)                                          |
| `neutro`      | FloatField | Probabilidade de neutralidade (neutral)                                      |
| `triste`      | FloatField | Probabilidade de tristeza (sad)                                              |
| `surpresa`    | FloatField | Probabilidade de surpresa (surprise)                                         |

---

## Diagrama de Relacionamentos

```
Contratos ──< Escolas ──< Locais >── Cameras ──< NotaFiscal
    │                                    │
    └──< Escalas ──< Tarefas >───────────┘
                                         │
                                    Processamentos ──< Faces
                                         │                │
Pessoas ──< Fotos             FrequenciasEscolar    ImagensTratadas
    │                                               FacesVerify >── Pessoas
    └──< Aluno >── Turmas >── Escolas               FacesPrevisaoEmocional
```

---

## Consequências

### Positivas

- **Separação de responsabilidades**: a divisão em três apps (`cadastros`, `cameras`, `analytical`) reflete o fluxo de dados do sistema — cadastro → captura → análise — e facilita a manutenção independente de cada domínio.
- **Rastreabilidade**: o `baseModel` abstrato garante que toda entidade registre automaticamente quando foi criada e atualizada, sem repetição de código.
- **Controle de limites**: a validação de limite de 10 fotos por pessoa na entidade `Fotos` centraliza a regra de negócio na camada de modelo.
- **Auditabilidade**: os campos `auditado` em `Faces`, `FacesVerify` e `FacesPrevisaoEmocional` permitem um fluxo de revisão humana sobre os resultados da IA.
- **Reprocessamento resiliente**: o campo `retry` em `Processamentos` permite controlar tentativas de reprocessamento sem perda de rastreabilidade.

### Negativas / Limitações

- **Credenciais em texto simples**: o modelo `Cameras` armazena `usuario` e `senha` em campos `CharField` sem criptografia. É necessário aplicar criptografia em nível de aplicação ou usar um gerenciador de segredos.
- **Caminhos de arquivo como string**: `Processamentos.path` e `Faces.path_face` armazenam caminhos no sistema de arquivos como strings. Isso acopla o banco de dados à estrutura de diretórios do servidor e pode causar problemas em deploys distribuídos ou em nuvem.
- **Ausência de FK entre `FacesPrevisaoEmocional` e `Faces`**: a entidade `FacesPrevisaoEmocional` não possui uma chave estrangeira explícita para `Faces`, dificultando a rastreabilidade da análise emocional até a face de origem.
- **Campo `periodo` com limite de tamanho ampliado em `Escalas`**: `periodo` foi originalmente definido como `CharField(max_length=10)`. O valor `'Período 9'` tem 9 caracteres e caberia no limite original, mas valores como `'Período 10'` (11 caracteres) excederiam o limite caso o domínio evolua para dois dígitos. O campo foi atualizado para `max_length=15` para acomodar essa expansão com margem.
- **`baseModel` duplicado**: cada app define seu próprio `baseModel` abstrato. Seria mais consistente centralizar essa classe em um módulo compartilhado (ex.: `core/base/models.py`).
