# Arquitetura do Sistema SecEdu Face

A arquitetura do sistema é desenhada num modelo de Microsserviços assíncronos guiados a eventos (Message-Driven), separando estritamente a UI administrativa, do worker de captura de eventos FTP, e do cluster de inferência de ML.

## Dívidas Técnicas Identificadas
1. **Ausência de Contratos de Testes:** Não identificamos suítes sólidas de testes em `server-jobs-faces`.
2. **Dependência Forte no Sistema de Arquivos (FTP):** O uso de diretórios aninhados como gatilho principal de eventos torna o sistema frágil a falhas de I/O e permissões.

Os diagramas detalhados estão nas páginas C4 adjacentes.
