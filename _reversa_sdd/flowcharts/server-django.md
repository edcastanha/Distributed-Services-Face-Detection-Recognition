```mermaid
graph TD
    A[Usuário/Admin] -->|Acessa Painel| B(Django Views)
    B --> C{Autenticação}
    C -->|Falha| D[Redireciona Login]
    C -->|Sucesso| E[Carrega Contexto do Banco]
    E --> F[Renderiza Template HTML]
```
