# Sistema de Atualização Cadastral no Terminal - Documentação de Dados

## 1. Estrutura
A pasta de dados possui duas pastas para lidar com banco e solicitações, já que tratam-se de coisas diferentes e, extensão/formato diferentes. Além disso, um arquivo banco.py solto na pasta contém funções e classes úteis para quem precisar usar o banco de dados SQL de clientes:
```text
└─ dados/
   ├─ banco/
   │  ├─ banco.db
   │  └─ schema.sql
   ├─ solicitacoes/
   │  └─ solicitacoes.json
   └─ banco.py
```

## 2. Bancos
A aplicação contém dois tipos de banco de dados para propósitos diferentes: armazenar clientes e usuários; armazenar solicitações. O banco de solicitações é uma lista JSON, que cada índice possui um dicionário. Já o banco de clientes e usuários é um SQLite.

### 2.1. Banco SQLite
Este será chamado no documento também como `banco.db` para facilitar a referência. A pasta `banco/` possui dois arquivos: `banco.db` e `schema.sql`, `schema.sql` é um arquivo de configuração para o banco que será criado, `banco.db` é o arquivo em que estão (ou que estarão) os clientes e usuários.

Fora da pasta `banco/`, existe `banco.py`, com funções escritas para consulta e criação do banco. Neste arquivo, existem duas classes: `Banco` e `BuscarNoBanco`. `Banco` possui 3 métodos:
- O método estático `obter_conexao()` cria uma conexão e retorna conexão e cursor, necessários para qualquer operação no banco.
- `criar_banco(cls)` é um classmethod que utiliza a função `obter_conexao()` para sua execução. Este método abre o arquivo `dados/schema.sql`, guarda cada linha em uma variável para depois executar com o cursor do banco e criá-lo.
- Por fim, `adicionar_cadastros_teste(cls)`, também um classmethod, apenas adiciona uma quantia fixa de 90 clientes de teste com dados aleátorios (não tão aleátorios) ao banco.

Um exemplo de uso da classe `Banco`:
```bash
banco = Banco()
conexao, cursor = banco.obter_conexao()
banco.criar_banco()
banco.adicionar_cadastros_teste()
```
Já a classe `BuscarNoBanco` possui:
- Um método `__init__` para definição de dois atributos: `_conexao` e `_cursor`, sendo que ambos referem-se aos dados obtidos pela função `Banco.obter_conexao()`.
- O método `buscar_cliente_por_nome(self, nome)`, que realiza uma consulta **parcial** no banco para encontrar um registro com o nome passado como argumento, isto significa que **mais de um registro pode ser encontrado**. Esta função retorna um dicionário com os dados encontrados.
- O método `buscar_cliente_por_cpf(self, cpf)`, que realiza uma consulta no banco para encontrar um registro com o **exato mesmo** CPF passado como argumento. Esta função retorna um dicionário com os dados encontrados.
- O método `buscar_acesso(self, usuario, email, senha)`, que realiza uma consulta no banco para encontrar um registro com os **exatos mesmos**: nome de usuário, email e senha passados como argumentos. Esta função possui dois tipos de retorno: um `False` caso encontre nada, ou um dicionário com os dados encontrados.
- O método `fechar_conexao(self)`, que encerra a conexão com o banco de dados.

Um exemplo de uso da classe `BuscarNoBanco`:
```bash
buscas = BuscarNoBanco(conexao, cursor)
cliente1 = buscas.buscar_cliente_por_nome(nome='test76')
cliente2 = buscas.buscar_cliente_por_cpf(cpf='01286712398')
acesso = buscar_acesso(usuario='ga', email='ga@email.com', senha='ga-senha_segura')
buscas.fechar_conexao()
```

### 2.2. Banco JSON