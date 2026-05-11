# Gerenciamento de Estoque

Um sistema de gerenciamento de estoque construído em Python com interface gráfica usando Tkinter e banco de dados SQLite.

## Integrantes do Grupo

- Fábio Macieira
- Ragila Ingrid
- Thiago Silva

## Funcionalidades

O projeto implementa as quatro operações básicas de banco de dados (CRUD) e uma funcionalidade de auditoria:
- **Adicionar:** Cadastro de novos produtos com Nome, Quantidade e Preço.
- **Visualizar:** Listagem de todos os produtos cadastrados exibidos em uma tabela (Treeview).
- **Atualizar:** Modificação dos dados de produtos já existentes no banco de dados.
- **Excluir:** Remoção de produtos do estoque.
- **Log de Auditoria:** Toda vez que um produto é excluído, um registro é gravado automaticamente no arquivo texto `auditoria.txt`, registrando a data, a hora, o ID, o nome, a quantidade e o preço do item deletado.

## Tecnologias Utilizadas

- **Python 3**
- **Tkinter** (Interface Gráfica e Componentes `ttk`)
- **SQLite3** (Banco de Dados Embutido)
- **Datetime** (Geração de timestamps para os logs)

## Estrutura do Projeto

- `app.py`: Arquivo principal contendo a lógica de conexão com banco de dados, funções CRUD e a interface gráfica completa da aplicação.
- `estoque.db`: Arquivo do banco de dados SQLite (gerado automaticamente na primeira execução).
- `auditoria.txt`: Arquivo de texto gerado para armazenar o histórico de produtos deletados.

## Como Executar

1. Certifique-se de ter o Python 3 instalado em seu computador.
2. Navegue até o diretório do projeto: `c:\Projetos\Trabalho_RAD`
3. Execute o script principal:
   ```bash
   python app.py
   ```

## Sobre o Desenvolvimento (RAD)

Este protótipo foi desenvolvido de acordo com os princípios do *Rapid Application Development* (RAD). O uso do Tkinter para a construção de interfaces (sem necessidade de setup complexo) aliado ao SQLite permitiu que a aplicação funcional com todos os requisitos fosse finalizada rapidamente, pronta para uso ou expansões e refinamentos futuros.
