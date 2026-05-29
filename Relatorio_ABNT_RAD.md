# RELATÓRIO TÉCNICO - SISTEMA DE GERENCIAMENTO DE ESTOQUE

## Capa

Instituição: [Preencher nome da instituição]

Curso: [Preencher nome do curso]

Disciplina: [Preencher nome da disciplina]

Projeto: Sistema de Gerenciamento de Estoque

Integrantes:
- Maguin
- Neguinho

Professor(a): [Preencher nome do professor(a)]

Cidade: [Preencher cidade]

Ano: 2026

---

## Resumo

Este relatório apresenta o desenvolvimento de um sistema de gerenciamento de estoque, implementado em Python, com interface gráfica em Tkinter e persistência de dados em banco SQLite. O projeto foi construído com base nos princípios de Rapid Application Development (RAD), priorizando rapidez de prototipação, simplicidade de manutenção e aderência aos requisitos funcionais da disciplina. O sistema permite incluir, listar, atualizar e excluir produtos, além de registrar auditoria textual de operações de inserção, atualização e exclusão no arquivo auditoria.txt, utilizando padrão de data e hora no formato brasileiro. A interface foi estruturada no modelo procedural, sem uso de classe para a camada visual, em conformidade com o padrão solicitado no projeto.

Palavras-chave: Python. Tkinter. SQLite. CRUD. Auditoria.

---

## 1 Introdução

A informatização do controle de estoque é essencial para reduzir erros de registro, facilitar consultas de produtos e oferecer maior confiabilidade no acompanhamento de movimentações. No contexto acadêmico, o desenvolvimento de um sistema desse tipo contribui para a prática de conceitos fundamentais de programação, banco de dados e design de interface.

Neste projeto, foi implementado um sistema desktop com recursos de cadastro e manutenção de produtos, apresentando dados em formato tabular com componente Treeview. Além das operações de CRUD, foi incluído um mecanismo de auditoria em arquivo texto para registrar as principais ações realizadas no sistema.

---

## 2 Objetivos

### 2.1 Objetivo Geral

Desenvolver uma aplicação desktop para gerenciamento de estoque com persistência em banco de dados local e registro de auditoria das operações.

### 2.2 Objetivos Específicos

- Implementar operações de inclusão, consulta, atualização e exclusão de produtos.
- Exibir produtos em tabela Treeview com cabeçalhos e alinhamentos padronizados.
- Validar dados de entrada para garantir consistência de quantidade e preço.
- Registrar logs de auditoria em formato textual padronizado.
- Estruturar a interface no modelo procedural, conforme padrão didático solicitado.

---

## 3 Fundamentação e Tecnologias Utilizadas

As tecnologias utilizadas foram selecionadas pela simplicidade de uso, integração nativa e adequação ao contexto de prototipação rápida:

- Python 3: linguagem principal para implementação da lógica e da interface.
- Tkinter e ttk: criação da interface gráfica e da tabela Treeview.
- SQLite3: banco de dados relacional embarcado para armazenamento local.
- Datetime: geração de data e hora para o sistema de auditoria.

A abordagem RAD orientou o ciclo de construção do projeto, permitindo evolução incremental com validações frequentes da interface e dos fluxos de uso.

---

## 4 Desenvolvimento do Sistema

### 4.1 Estrutura Geral

O sistema foi implementado em um único arquivo principal (app.py), contendo:

- Configuração da base de dados e criação automática da tabela de produtos.
- Funções de acesso ao banco para operações CRUD.
- Funções de interface para eventos dos botões e seleção de itens na tabela.
- Função de auditoria para escrita no arquivo auditoria.txt.

### 4.2 Modelagem de Dados

A tabela produtos contém os seguintes campos:

- id (INTEGER, chave primária autoincremento)
- nome (TEXT, não nulo)
- quantidade (INTEGER, não nulo)
- preco (REAL, não nulo)

### 4.3 Interface Gráfica

A janela principal foi configurada com título "Painel de Controle de Estoque" e dimensão 600x350. A interface possui:

- Campos de entrada: Produto, Quantidade e Preço.
- Botões de ação: Incluir, Atualizar, Apagar e Limpar.
- Tabela Treeview com colunas:
  - ID
  - Descrição do Produto
  - Qtd em Estoque
  - Preço Unitário

Padrão de largura e alinhamento da tabela:

- id: largura 50, centralizado.
- nome: largura 250, alinhado à esquerda.
- qtd: largura 100, centralizado.
- preco: largura 120, centralizado.

### 4.4 Validação de Dados

Antes de operações de inclusão e atualização, o sistema valida:

- Preenchimento obrigatório de todos os campos.
- Quantidade como número inteiro.
- Preço como valor numérico decimal.

### 4.5 Auditoria

O sistema registra logs no arquivo auditoria.txt para as ações de inserção, atualização e exclusão, com data e hora no formato dd/mm/aaaa hh:mm:ss.

Exemplos de linhas geradas:

- [05/05/2026 14:30:15] INSERÇÃO - Produto "Monitor" (Qtd: 10) cadastrado com sucesso.
- [05/05/2026 15:45:00] ATUALIZAÇÃO - Produto "Monitor" alterado (Nova Qtd: 8, Novo Preço: 850.00).
- [06/05/2026 09:12:30] EXCLUSÃO - Produto "Teclado Mecânico" removido do sistema.

---

## 5 Resultados e Discussão

O sistema atendeu aos requisitos propostos para o projeto, com execução estável das operações CRUD e atualização visual imediata da tabela após cada ação. A auditoria textual ampliou a rastreabilidade das mudanças no estoque, contribuindo para controle e transparência.

A escolha por arquitetura procedural para a interface permitiu aderência ao padrão solicitado, com código direto e fácil leitura para fins didáticos. Como limitação, o sistema ainda não possui autenticação de usuários, controle de permissões ou geração de relatórios analíticos.

---

## 6 Testes do Sistema

Para validação funcional do protótipo, foram realizados testes manuais orientados por casos de uso principais:

- Teste de inclusão: inserção de produto com dados válidos, verificando gravação no banco e atualização imediata da tabela.
- Teste de validação: tentativa de inclusão com campos vazios e com quantidade/preço inválidos, verificando mensagens de aviso e bloqueio da operação.
- Teste de atualização: alteração de quantidade e preço de item existente, confirmando persistência no banco e atualização visual no Treeview.
- Teste de exclusão: remoção de item selecionado, com confirmação do usuário e retirada do registro da tabela.
- Teste de auditoria: verificação das entradas no arquivo auditoria.txt para INSERÇÃO, ATUALIZAÇÃO e EXCLUSÃO no formato dd/mm/aaaa hh:mm:ss.

Resultado dos testes: os fluxos principais do sistema foram executados com sucesso e sem falhas críticas, atendendo aos requisitos funcionais da versão atual.

---

## 7 Visão de Futuro (Versão 2.0)

Seguindo a abordagem RAD de evolução incremental, as duas primeiras funcionalidades de negócio recomendadas para o próximo ciclo são:

1. Gestão de Compras e Reposição

Implementar controle de entradas por fornecedor, com registro de custo de aquisição, data de compra e sugestão de reposição com base em estoque mínimo. Essa funcionalidade melhora o planejamento de abastecimento e reduz risco de ruptura.

2. Módulo de Vendas e Saída de Estoque

Adicionar registro de saídas por venda, com abatimento automático do estoque e histórico de movimentações. Essa funcionalidade permite acompanhar giro de produtos, apoiar decisões comerciais e preparar o sistema para relatórios de faturamento e margem.

---

## 8 Conclusão

Conclui-se que o desenvolvimento da aplicação alcançou o objetivo de implementar um sistema funcional de gerenciamento de estoque com interface gráfica, persistência em banco de dados local e mecanismo de auditoria padronizado. O projeto demonstrou, na prática, a integração entre interface, banco de dados e validações, consolidando competências importantes para aplicações administrativas de pequeno porte.

Como continuidade, recomenda-se adicionar filtros de pesquisa, exportação de dados e melhorias de usabilidade para fortalecer o potencial de uso do sistema em cenários mais amplos.

---

## 9 Referências

PYTHON SOFTWARE FOUNDATION. Python Language Reference. Disponível em: https://docs.python.org/3/. Acesso em: 29 maio 2026.

PYTHON SOFTWARE FOUNDATION. tkinter - Python interface to Tcl/Tk. Disponível em: https://docs.python.org/3/library/tkinter.html. Acesso em: 29 maio 2026.

SQLITE. Documentation. Disponível em: https://www.sqlite.org/docs.html. Acesso em: 29 maio 2026.

---

## 10 Apêndice A - Estrutura dos Arquivos do Projeto

- app.py
- estoque.db
- auditoria.txt
- Relatorio_RAD.pdf
