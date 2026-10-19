# PetVida - Conexão Python com SQL Server

## Descrição

Projeto desenvolvido para a disciplina de Banco de dados Avançado.

O objetivo do projeto é implementar uma camada de acesso a dados em Python para o banco de dados PetVida , utilizando SQL Server e a biblioteca pyodbc.

O sistema permite realizar operações relacionadas a tutores , pets , consultas veterinárias e procedimentos.

## Tecnologias utilizadas 
- Python 
- SQL Server
- pyodbc
- ODBC Driver 18 for SQL Server

## Estrutura do projeto
- `db.py` - responsável pela conexão com o SQL Server e controle das transações.
- `repositorio.py` - contém as operações de acesso ao banco de dados.
- `main.py` - menu de terminal para utilização das funções do repositório.
- `README.md` - documentação do projeto.

## Configuração do banco de dados
Antes de executar o projeto , é necessário executar no SQL Server o script `01_estrutura_petvida.sql` fornecido pelo porfessor.

O projeto utiliza o banco:
PetVida

A conexão foi configurada utilizando autenticação do Windows e ODBC Driver 18 for SQL Server.

Configuração utilizada :
- Servidor : `localhost\SQLEXPRESS`
- Banco de dados : `PetVida`
- Autenticação : Windows Authentication
- Driver : ODBC Driver 18 for SQL Server

Não são armazenados usuário ou senha diretamente no código.

## Instalação
É necessário ter o Python instalado e instalar a biblioteca pyodbc.

No terminal:
```bash
pip install pyodbc
```
Também é necessário possuir o ODBC Driver 18 for SQL Server instalado.

## Como executar
Abra o terminal na pasta do projeto e execute:
```bash
python main.py
```
O menu do sistema ser´´a apresentado no terminal.

## Funcionalidades
O projeto possui operações para:
- cadastrar, buscar, listar, atualizar e excluir tutores;
- cadastrar, atualizar, transferir e excluir pets;
- listar os pets de um tutor;
- buscar um pet juntamente com seu tutor;
- agendar consultas;
- adicionar e remover procedimentos;
- listar procedimentos de uma consulta;
- listar consultas por procedimento;
- calcular o valor total de uma consulta;
- atualizar o status de uma consulta;
- excluir consultas;
- consultar o histórico de um pet.

## Segurança
Os valores recebidos pelas operações SQL são enviados utilizando
comandos parametrizados com `?`, evitando a concatenação direta dos
dados do usuário no SQL.

As conexões são abertas somente quando necessárias e fechadas após
a execução das operações.

As transações utilizam `commit` quando a operação é concluída com
sucesso e `rollback` quando ocorre algum erro.

No comando de atualização de tutor, os nomes das colunas são
controlados por uma lista de campos permitidos.

## Bônus
Foram implementados os dois itens bônus da atividade:
- histórico do pet utilizando a view `vw_resumo_consulta`;
- menu de terminal no arquivo `main.py`