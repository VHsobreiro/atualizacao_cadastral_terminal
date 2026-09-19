import os
import sqlite3
from dotenv import load_dotenv
from random import randint
import logging

load_dotenv()

CAMINHO_BANCO_DB = os.getenv('CAMINHO_BANCO_DB')
CAMINHO_SCHEMA_SQL = os.getenv('CAMINHO_SCHEMA_SQL')

logger = logging.getLogger(__name__)

class Banco:
    @staticmethod
    def obter_conexao():
        try:
            conexao = sqlite3.connect(CAMINHO_BANCO_DB)
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            logger.info('Conexão com o banco de dados obtida com sucesso')
            return (conexao, cursor)
        except Exception as erro:
            logger.error(f'Ocorreu um erro ao obter a conexão com o banco de dados: {erro}', exc_info=True)
            raise

    @classmethod
    def criar_banco(cls):
        conexao, cursor = cls.obter_conexao()
        with open(CAMINHO_SCHEMA_SQL, 'r', encoding='utf-8') as schema:
            schema_sql = schema.read()

        cursor.executescript(schema_sql)
        conexao.commit()
        conexao.close()
        logger.info('Banco de dados criado com sucesso')

    @classmethod
    def adicionar_cadastros_teste(cls):
        conexao, cursor = cls.obter_conexao()

        for i in range(90):
            nome = f'test{i}'
            cpf = ''
            for _ in range(11):
                cpf += str(randint(0, 9))
            salario = None
            veiculo = None
            endereco = None
            casa_propria = False

            atualizacao = randint(0, 2)

            match(atualizacao):
                case 0: # Atualização de Renda
                    salario = randint(1621, 16210)
                case 1: # Atualização de Patrimônio
                    patrimonio = randint(3, 5)
                    if patrimonio == 3: # IPVA
                        veiculo = f'PL{randint(10, 99)}'
                    elif patrimonio == 4: # IPTU
                        endereco = f'Quadra {randint(1, 18)}, Conjunto X, Casa {randint(1, 60)}'
                    else: # IPVA E IPTU
                        veiculo = f'X{randint(0, 9)}AM'
                        casa_propria = True
                        endereco = f'Quadra {randint(1, 18)}, Casa {randint(1, 60)}'
                case 2: # Atualização de Endereço
                    endereco = f'Condominio do Bem, Rua {randint(1, 18)}, Casa {randint(1, 60)}'
                    
            cursor.execute('INSERT INTO clientes (nome, cpf, salario, veiculo, endereco, casa_propria) VALUES (?, ?, ?, ?, ?, ?)', (nome, cpf, salario, veiculo, endereco, casa_propria))

        conexao.commit()
        conexao.close()
        print('Cadastros adicionados com sucesso!')

class BuscarNoBanco:
    def __init__(self, conexao, cursor):
        self._conexao = conexao
        self._cursor = cursor

    def buscar_cliente_por_nome(self, nome):
        self._cursor.execute('SELECT * FROM clientes WHERE nome LIKE ?', (nome,))
        dados_sql = self._cursor.fetchall()
        busca = None
        for linha in dados_sql:
            busca = dict(linha)
        return busca
    
    def buscar_cliente_por_cpf(self, cpf):
        self._cursor.execute('SELECT * FROM clientes WHERE cpf = ?', (cpf,))
        dados_sql = self._cursor.fetchone()
        busca = None
        for linha in dados_sql:
            busca = dict(linha)
        return busca
    
    def buscar_acesso(self, usuario, email, senha):
        self._cursor.execute('SELECT * FROM acessos WHERE usuario = ? AND email = ? AND senha = ?', (usuario, email, senha))
        dados_sql = self._cursor.fetchone()
        if not dados_sql:
            return False
        busca = dict(dados_sql)

        return busca
    
    def fechar_conexao(self):
        self._conexao.close()
