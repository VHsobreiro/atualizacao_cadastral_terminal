from dados.solicitacoes import solicitacoes

def editar_solicitacao(id_da_solicitacao, acesso):
    lista_de_solicitacoes = solicitacoes.abrir_solicitacoes()

    for solicitacao in lista_de_solicitacoes:
        if not id_da_solicitacao == solicitacao['id']:
            continue

        print(f"ID: {solicitacao['id']}")

        cliente = input(f"Cliente (salvo: {solicitacao['cliente']}): ").strip()
        if cliente:
            solicitacao['cliente'] = cliente

        tipo = input(f"Tipo (salvo: {solicitacao['tipo']}): ").strip()
        if tipo:
            solicitacao['tipo'] = tipo

        print(f"Criado por: {solicitacao['criado_por']}")

        dados_antigos = input(f"Dados antigos (salvo: {solicitacao['dados_antigos']}): ").strip()
        if dados_antigos:
            solicitacao['dados_antigos'] = dados_antigos

        dados_novos = input(f"Dados novos (salvo: {solicitacao['dados_novos']}): ").strip()
        if dados_novos:
            solicitacao['dados_novos'] = dados_novos

        print(f"Histórico (salvo: {solicitacao['historico']})")

        solicitacao['status'] = "AGUARDANDO_GA"

        solicitacao['historico'].append({
            "acao": "editado",
            "usuario": acesso.get('usuario'),
            "status": "AGUARDANDO_GA"
        })

        solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
        print("Solicitação atualizada com sucesso!")
        return

    print("Solicitação não encontrada.")
    print("Solicitação encontrada.")
    
    
