import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dados.solicitacoes.solicitacoes import abrir_solicitacoes, salvar_solicitacao

def ver_dados_antigos(id_solicitacao):
    solicitacoes = abrir_solicitacoes()

    for solicitacao in solicitacoes:
        if solicitacao["id"] == id_solicitacao:

            print("\n=== DADOS ANTIGOS ===")

            dados = solicitacao.get("dados_antigos", {})

            for campo, valor in dados.items():
                print(f"{campo}: {valor}")

            return dados

    print("Solicitação não encontrada.")
    return None


def ver_dados_novos(id_solicitacao):
    solicitacoes = abrir_solicitacoes()

    for solicitacao in solicitacoes:
        if solicitacao["id"] == id_solicitacao:

            print("\n=== DADOS NOVOS ===")

            dados = solicitacao.get("dados_novos", {})

            for campo, valor in dados.items():
                print(f"{campo}: {valor}")

            return dados

    print("Solicitação não encontrada.")
    return None

def ver_tipo_atualizacao(id_solicitacao):
    solicitacoes = abrir_solicitacoes()

    for solicitacao in solicitacoes:
        if solicitacao["id"] == id_solicitacao:

            tipo = solicitacao.get("tipo_atualizacao")

            print(f"Tipo de atualização: {tipo}")

            return tipo

    print("Solicitação não encontrada.")
    return None
    
