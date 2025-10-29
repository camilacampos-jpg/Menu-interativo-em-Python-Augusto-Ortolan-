# Sistema de Cadastro de Alunos

## Integrantes do Grupo
* **Camila Campos** - RA 1118454
* **Mathias Karling Stadtlober** - RA 1116251
* **Grazieli da Silva** - RA 1069517

## Tema
Sistema de Cadastro de Alunos

## Descrição do Sistema
O Sistema de Cadastro de Alunos em Python tem como objetivo registrar nome, curso e média final, informação estudantis de forma simples rápida e eficiente. O projeto contem um arquivo principal chamado **main.py**, que executa o menu do sistema.

## Tecnologias Utilizadas
* Linguagem de Programação: Python
* Controle de Versão: Git e GitHub
* Persistência de Dados: Arquivo de texto (.txt)

## Funcionalidades do Sistema
O sistema apresenta um menu principal com as seguintes opções:

1.  **Cadastro do aluno** (Implementa a função `cadastrar nome do aluno_item`)
2.  **Lista** (Implementa a função `listar curso_itens`)
3.  **Editar** (Implementa a função `editar nota_item`)
4.  **Excluir** (Implementa a função `excluir nota_item`)
5.  **Sair**

O programa permanece em execução até que o usuário escolha explicitamente Sair.

## Persistência de Dados
* Os dados são armazenados no arquivo `dados/cadastros.txt`.
* Logs de execução (ação, data e hora) são registrados no arquivo `log.txt`.

## Como Executar
1.  Garanta a estrutura de pastas: **`Sistema_Cadastro_Alunos/dados/`**.
2.  Execute o arquivo `main.py` usando o comando no terminal: `python main.py`