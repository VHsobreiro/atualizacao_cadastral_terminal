import json
from dotenv import load_dotenv
import os

load_dotenv()
CAMINHO_SOLICITACOES= os.getenv("CAMINHO_SOLICITACOES")


def abrir_solicitacoes():
    with open(CAMINHO_SOLICITACOES, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    

def salvar_solicitacao(solicitacoes):
    with open (CAMINHO_SOLICITACOES, "w", encoding="utf-8") as arquivo:
        return json.dump(solicitacoes, arquivo, indent=4, ensure_ascii = False)
    

def adicionar_solicitacao(nova_solicitacao):
    solicitacoes = abrir_solicitacoes()
    solicitacoes.append(nova_solicitacao)
    salvar_solicitacao(solicitacoes)

def atualizar_status_solicitacao(id_solicitacao, novo_status,usuario_acao, observacao=""):
    solicitacoes = abrir_solicitacoes()

    solicitacao_encontrada = None
    for item in solicitacoes:
        if item["id"].upper() == id_solicitacao.upper():
            solicitacao_encontrada = item
            break

    if not solicitacao_encontrada:
        print(f" Solicitação {id_solicitacao} não foi encontrada!")
        return False
    
    
    solicitacao_encontrada["status"] = novo_status
    
    texto_acao = f"Status alterado para {novo_status}"
    if observacao:
        texto_acao += f" - Obs: {observacao}"

    solicitacao_encontrada["historico"].append({
        "acao": texto_acao,
        "usuario": usuario_acao,
        "status": novo_status
    })

    salvar_solicitacao(solicitacoes)
    print(f"Status da solicitação {id_solicitacao} atualizado para {novo_status}!")
    return True
