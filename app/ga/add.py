from dados.solicitacoes.solicitacoes import abrir_solicitacoes
from dados.solicitacoes.solicitacoes import salvar_solicitacao





def ga():
    while True:
        print('painel do GA ')
        print('''
    1 - visualizar solicitaçôes pendende
    2 - consultar solicitação 
    3 - sair 
        ''')
        
        while (opcao := input("escolha um opcao: ").strip()) not in ["1" , "2", "3"]: print("opcao invalida! tente novamente" )

        if opcao == "1":
            if visualizar_solicitacoes_pedente("AGUARDANDO_GA"):
                id = input("digite o ID da solicitação: ")
                print("1 - aprovar | 2 - reprovar | 3 - pedir ajuste para o GN")
                acao = input("escolha: ")
                if acao == "1":
                    atualizar_status_solicitacao(id, "AGUARDANDO_CAD", usuario)
                if acao == "2":
                    atualizar_status_solicitacao(id, "REPROVADO", usuario, input("Motivo: "))
                if acao == "3":
                    atualizar_status_solicitacao(id, "PENDENTE_AJUSTE_GN", usuario, input("Qual ajuste: "))
        elif opcao == "2":
            consultar_historico(input("digite o id: " ))
             

                    


# visualiza as solicitações de acordo com o status EX: AGUARDANDO_GA
def visualizar_solicitacoes_pedente(status_filtro=None):
    solicitacoes = abrir_solicitacoes()
    filtra = [s for s in solicitacoes if s["status"] == status_filtro] if status_filtro else solicitacoes  
    if not filtra: 
        print("\n nenhuma solicitação encontrada! " )
        return False

    for s in filtra:
        print(f"ID: {s['id']} | Cliente: {s['cliente']} | Tipo: {s['tipo']} | Status: {s['status']}  ")
        print(f"De: {s['dados_antigos']} Para: {s['dados_novos']} ") 
        return True
    
# atualiza status EX:AGUARDANDO_GA para AGUARDANDO_CAD
def atualizar_status_solicitacao(id_solicitacao, novo_status, usuario_acao, observacao=""):

    solicitacoes = abrir_solicitacoes() 
    solicitacao = next((s for s in solicitacoes if s["id"].upper() == id_solicitacao.upper()), None)

    if not solicitacao:
        print(f"solicitaçao {id_solicitacao} não foi encontrado")
        return False
    
    solicitacao["status"] = novo_status
    texto_acao = f"status alterado para {novo_status}"
    if observacao:
        texto_acao += f" - obs: {observacao}"

    solicitacao["historico"].append({
        "acao": texto_acao,
        "usuario": usuario_acao,
        "status": novo_status
    })

    salvar_solicitacao(solicitacoes)
    print(f"status da {id_solicitacao} alterado para {novo_status}")
    return True


# consulta histórico de acordo com o ID
def consultar_historico(id_solicitacao):
    solicitacoes = abrir_solicitacoes()
    solicitacao = next((s for s in solicitacoes if s["id"].upper() == id_solicitacao.upper()), None)
    
    if not solicitacao:
        print(f"solicitaçao {id_solicitacao} não foi encontrado")
        return False

    print("\n" + "="*50)
    print(f"   HISTÓRICO COMPLETO DA SOLICITAÇÃO: {solicitacao['id']}")
    print("="*50)
    print(f"Cliente: {solicitacao['cliente']} | Tipo: {solicitacao['tipo']} | Status Atual: {solicitacao['status']}")
    print(f"Dados Antigos: {solicitacao['dados_antigos']}")
    print(f"Dados Novos:   {solicitacao['dados_novos']}")
    print("-" * 50)
    print("Linha do tempo de alterações:")
    for i, h in enumerate(solicitacao["historico"], 1):
        print(f"  {i}. [{h['status']}] {h['acao']} (Por: {h['usuario']})")
    print("="*50)

