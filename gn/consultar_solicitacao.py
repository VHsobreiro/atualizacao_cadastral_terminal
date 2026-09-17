import os   
import sys

# Adiciona a pasta pai ao caminho de importação do Python
# Isso permite importar arquivos que estão em outras pastas do projeto

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importa a função responsável por abrir/carregar as solicitações

from dados.solicitacoes.solicitacoes import abrir_solicitacoes

# Função responsável por consultar uma solicitação pelo seu ID

def consultar_solicitacao(id_solicitacao):  
    solicitacoes = abrir_solicitacoes()

    for solicitacao in solicitacoes:
        if solicitacao["id"] == id_solicitacao:
            print(f"ID: {solicitacao['id']}")
            print(f"Cliente: {solicitacao['cliente']}")
            print(f"Tipo: {solicitacao['tipo']}")
            print(f"Status: {solicitacao['status']}")
            print(f"Criado por: {solicitacao['criado_por']}")
            print(f"Dados antigos: {solicitacao['dados_antigos']}")
            print(f"Dados novos: {solicitacao['dados_novos']}")
            print(f"Histórico: {solicitacao['historico']}")
            return solicitacao
        
    # Caso nenhuma solicitação com o ID informado seja encontrada,
    # exibe uma mensagem avisando

    print(f"Solicitação {id_solicitacao} não foi encontrada!")

    #retorna none avisando que nao encontrou nenhuma solicitacao 

    return None
