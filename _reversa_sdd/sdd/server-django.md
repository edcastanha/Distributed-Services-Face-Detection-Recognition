# Administração Web e Gateway (Django)

## Visão Geral
Este componente fornece a interface de usuário administrativa e o framework de modelos (ORM) usado para persistir as requisições geradas pelo cluster de identificação.

## Responsabilidades
- Prover a interface de portal/dashboard para gerenciar o SecEdu Face.
- Fornecer os schemas (Models) relacionais do banco principal.
- Acionar as subrotinas sob demanda ou gerenciar logs gerados pelo pipeline de processamento assíncrono.

## Interface
- **Entrada:** Interação de usuários administradores via HTTP (Browser).
- **Saída:** HTML dinâmico, chamadas para banco de dados relacional.

## Regras de Negócio
- Pessoas não autenticadas ou com perfis sem permissões não acessam o painel administrativo. 🟡
- Apenas logs estruturados e embeddings aprovados pelo Flask devem ser atrelados e visíveis. 🟡

## Fluxo Principal
1. O usuário final (Admin) navega para a tela de relatórios e embeddings de faces.
2. O Django processa a requisição acionando o Controller/View.
3. Consulta o Banco de Dados filtrando pelos modelos vinculados a câmeras e paths do FTP.
4. Renderiza a resposta com os metadados.

## Fluxos Alternativos
- **Acesso negado:** Redirecionamento automático para `/login/` em caso de falta de sessão.

## Dependências
- **PostgreSQL/MySQL (Relacional)** — Persistência a longo prazo.
- **Celery Workers** — Podem usar o código dos modelos deste diretório para conseguir registrar no banco os dados.

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Segurança | Autenticação padrão de sessão de framework. | Estrutura de pasta server-django | 🟡 |

> Inferido a partir do código. Validar com equipe de operações.

## Critérios de Aceitação

```gherkin
Dado que sou um administrador logado
Quando acesso o painel central de câmeras e logs
Então devo visualizar registros preenchidos pelo cluster de processamento backend
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Persistência e UI | Must | É a interface final para auditoria do usuário |
| Views Customizadas | Could | As telas HTML são úteis, mas a API em si é consumida de forma headless muitas vezes |

## Rastreabilidade de Código

| Arquivo | Função / Classe | Cobertura |
|---------|-----------------|-----------|
| `server-django` (Pasta Root) | Models/Views | 🟡 |

## Cenários de Borda
- **Base de Dados superlotada:** Quando há milhares de execuções do RabbitMQ gerando embeddings por segundo, a UI do Django na exibição de paginação pode ficar significativamente lenta sem caching adequado. 🟡
