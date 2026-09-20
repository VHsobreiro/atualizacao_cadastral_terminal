import logging

logger = logging.getLogger(__name__)

from app.dados import banco
from app.dados.solicitacoes import solicitacoes
from app.gn import consultar_solicitacao, criar_solicitacao, editar_solicitacao

banco_obj = banco.Banco()
conexao, cursor = banco_obj.obter_conexao()
buscador = banco.BuscarNoBanco(conexao=conexao, cursor=cursor)

solicitacao_obj = criar_solicitacao.SolicitacaoCadastro(buscador=buscador)

def consultar_solicitacoes(acesso):
    lista_de_solicitacoes = solicitacoes.abrir_solicitacoes()

    if not lista_de_solicitacoes:
        logger.error("Nenhuma solicitação encontrada na lista")
        return

    linhas = int(input('Quantidade de solicitações por página: '))
    try:
        if linhas <= 0:
            print('Quantidade inválida')
    except ValueError:
        print('Quantidade inválida')

    for linha, solicitacao in enumerate(lista_de_solicitacoes, start=1):
        print('-' * 10, f' SOLICITAÇÃO {linha} ', '-' * 10)
        print(f"ID: {solicitacao['id']}")
        print(f"Cliente: {solicitacao['cliente']}")
        print(f"Tipo: {solicitacao['tipo']}")
        print(f"Status: {solicitacao['status']}")
        print(f"Criado por: {solicitacao['criado_por']}")
        print(f"Dados antigos: {solicitacao['dados_antigos']}")
        print(f"Dados novos: {solicitacao['dados_novos']}")
        print(f"Histórico: ")
        for registro, mudanca in enumerate(solicitacao['historico'], start=1):
            print(' ' * 4, '=' * 5, f'REGISTRO {registro}', '=' * 5)
            print(' ' * 4, 'Ação: ', mudanca['acao'])
            print(' ' * 4, 'Usuário: ', mudanca['usuario'])
            print(' ' * 4, 'Status: ', mudanca['status'])

        if linha % linhas == 0 and linha < len(lista_de_solicitacoes):
            input('Pressione enter para continuar')

def main():
    tela_inicial()

    usuario = input('Digite seu nome: ')
    email = input('Seu email: ')
    senha = input('Agora sua senha: ')

    acesso = verificar_login(usuario=usuario, email=email, senha=senha)

    if not acesso:
        logger.warning(f'Login mal-sucedido do usuário {usuario}')

    logger.info(f'Login bem-sucedido do usuário {usuario}')

    logado = True
    while logado:
        match acesso.get('cargo'):
            case 'GN':
                logado = painel_gn(acesso=acesso)
            case 'GA':
                logado = painel_ga(acesso=acesso)
            case 'CAD':
                logado = painel_cad(acesso=acesso)

def tela_inicial():
    print('''
█▀ █ █▀ ▀█▀ █▀▀ █▀▄▀█ ▄▀█   █▀▄ █▀▀   ▄▀█ ▀█▀ █░█ ▄▀█ █░░ █ ▀█ ▄▀█ █▀▀ ▄▀█ █▀█
▄█ █ ▄█ ░█░ ██▄ █░▀░█ █▀█   █▄▀ ██▄   █▀█ ░█░ █▄█ █▀█ █▄▄ █ █▄ █▀█ █▄▄ █▀█ █▄█

█▀▀ ▄▀█ █▀▄ ▄▀█ █▀ ▀█▀ █▀█ ▄▀█ █░░   █▄░█ █▀█   ▀█▀ █▀▀ █▀█ █▀▄▀█ █ █▄░█ ▄▀█ █░░
█▄▄ █▀█ █▄▀ █▀█ ▄█ ░█░ █▀▄ █▀█ █▄▄   █░▀█ █▄█   ░█░ ██▄ █▀▄ █░▀░█ █ █░▀█ █▀█ █▄▄''')

    print('\n')
    print('Primeiro é necessário autenticar-se para acessar o sistema')

def verificar_login(usuario, email, senha):
    acesso = buscador.buscar_acesso(usuario=usuario, email=email, senha=senha)

    if not acesso:
        return False

    return acesso

def painel_gn(acesso):
    print('''
█▀█ ▄▀█ █ █▄░█ █▀▀ █░░   █▀▀ █▄░█
█▀▀ █▀█ █ █░▀█ ██▄ █▄▄   █▄█ █░▀█''')
    print('\n')
    print(f'Seja bem-vindo(a) ao sistema, {acesso.get('usuario')}')
    print('Selecione uma opção abaixo: ')
    print('[ 1 ] Criar solicitação')
    print('[ 2 ] Consultar solicitações')
    print('[ 3 ] Editar solicitação')
    print('[ 4 ] Encerrar programa')
    try:
        opcao = int(input('Sua opção: '))
        match opcao:
            case 1:
                gn_criar_solicitacao(acesso=acesso)
            case 2:
                consultar_solicitacoes(acesso=acesso)
            case 3:
                gn_editar_solicitacao(acesso=acesso)
            case 4:
                return False
                
    except ValueError:
        print('Escreva apenas números')

    return True

def gn_criar_solicitacao(acesso):
    identificador_cliente = input('Nome ou CPF do cliente: ')
    solicitacao_obj.buscar_cliente(identificador=identificador_cliente)

    print('Tipo de atualização')
    print('[1] Renda')
    print('[2] Patrimônio')
    print('[3] Endereço')

    try:
        tipo_de_atualizacao = input('Sua opção: ')
        solicitacao_obj.selecionar_tipo(opcao=tipo_de_atualizacao)
        solicitacao = solicitacao_obj.criar_solicitacao(
            usuario_logado=acesso,
            identificador_cliente=identificador_cliente,
            opcao_tipo=tipo_de_atualizacao)
        
        if not solicitacao:
            print(f"Falha ao criar solicitação: {solicitacao_obj.status}") 
            return
        
        print(f"Solicitação {solicitacao_obj.id} criada com sucesso!")
        print(solicitacao_obj.to_dict())
        
    except ValueError:
        print('Opção inválida, digite apenas números')

def gn_editar_solicitacao(acesso):
    id_da_solicitacao = input('ID da solicitação: ')

    if int(id_da_solicitacao) >= 0:
        if not consultar_solicitacao.consultar_solicitacao(id_da_solicitacao):
            return
        
        editar = input('Deseja editar essa solicitação [S/n]: ').lower().strip()

        match editar:
            case 's' | '':
                editar_solicitacao.editar_solicitacao(id_da_solicitacao, acesso=acesso)
            case 'n':
                return
            case _:
                print('Valor inválido')
    else:
        print('Selecione um ID válido')

def painel_ga(acesso):
    print('''
█▀█ ▄▀█ █ █▄░█ █▀▀ █░░   █▀▀ ▄▀█
█▀▀ █▀█ █ █░▀█ ██▄ █▄▄   █▄█ █▀█''')
    print('\n')
    print(f'Seja bem-vindo(a) ao sistema, {acesso.get('usuario')}')
    print('Selecione uma opção abaixo: ')
    print('[ 1 ] Consultar solicitações')
    print('[ 2 ] Analisar solicitação')
    print('[ 3 ] Encerrar programa')

    try:
        opcao = int(input('Sua opção: '))
        match opcao:
            case 1:
                consultar_solicitacoes(acesso=acesso)
            case 2:
                id = int(input('ID da solicitação: '))
                ga_analisar_solicitacao(id=id, acesso=acesso)
            case 3:
                return False
                    
    except ValueError:
        print('Escreva apenas números')
    
    return True

def ga_analisar_solicitacao(id, acesso):
    print('[ 1 ] Aprovar solicitação')
    print('[ 2 ] Reprovar solicitação')
    print('[ 3 ] Devolver solicitação para ajustes')
    print('[ 4 ] Voltar')
    try:
        opcao = int(input('Sua opção: '))
        if opcao == 4:
            return
        
        lista_de_solicitacoes = solicitacoes.abrir_solicitacoes()
        solicitacao = None

        for solicitacao_ in lista_de_solicitacoes:
            if not solicitacao_['id'] == id:
                continue

            solicitacao = solicitacao_
            break

        if not solicitacao:
            print(f'Solicitação com id {id} não encontrada') 
            return

        match opcao:
            case 1:
                solicitacao['status'] = 'ESPERANDO_CADASTRO'
                solicitacao['historico'].append({
                    'acao': 'Aprovado para análise final',
                    'usuario': acesso.get('usuario'),
                    'status': 'ESPERANDO_CADASTRO'
                })
                solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                print('Solicitação aprovada com sucesso')
            case 2:
                solicitacao['status'] = 'RECUSADO'
                solicitacao['historico'].append({
                    'acao': 'Reprovado',
                    'usuario': acesso.get('usuario'),
                    'status': 'RECUSADO'
                })
                solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                print('Solicitação recusada com sucesso')
            case 3:
                solicitacao['status'] = 'AJUSTE_GN'
                solicitacao['historico'].append({
                    'acao': 'Devolvido para ajuste pelo GA',
                    'usuario': acesso.get('usuario'),
                    'status': 'AJUSTE_GN'
                })
                solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                print('Solicitação devolvida para ajustes com sucesso')
            case _:
                print('Valor inválido')
        
    except ValueError:
        print('Escreva apenas números')

def painel_cad(acesso):
    print('''
█▀█ ▄▀█ █ █▄░█ █▀▀ █░░   ▀█▀ █ █▀▄▀█ █▀▀   █▀▄ █▀▀   █▀▀ ▄▀█ █▀▄ ▄▀█ █▀ ▀█▀ █▀█ █▀█
█▀▀ █▀█ █ █░▀█ ██▄ █▄▄   ░█░ █ █░▀░█ ██▄   █▄▀ ██▄   █▄▄ █▀█ █▄▀ █▀█ ▄█ ░█░ █▀▄ █▄█''')
    print('\n')
    print(f'Seja bem-vindo(a) ao sistema, {acesso.get('usuario')}')
    print('[ 1 ] Consultar solicitações')
    print('[ 2 ] Analisar solicitação')
    print('[ 3 ] Encerrar programa')

    try:
        opcao = int(input('Sua opção: '))
        match opcao:
            case 1:
                consultar_solicitacoes(acesso=acesso)
            case 2:
                id = int(input('ID da solicitação: '))
                cad_analisar_solicitacao(id=id, acesso=acesso)
            case 3:
                return False
                    
    except ValueError:
        print('Escreva apenas números')
    
    return True

def cad_analisar_solicitacao(acesso, id):
    print('[ 1 ] Efetivar solicitação')
    print('[ 2 ] Reprovar solicitação')
    print('[ 3 ] Devolver solicitação para ajustes')
    print('[ 4 ] Voltar')
    try:
        opcao = int(input('Sua opção: '))
        if opcao == 4:
            return
        
        lista_de_solicitacoes = solicitacoes.abrir_solicitacoes()
        solicitacao = None

        for solicitacao_ in lista_de_solicitacoes:
            if not solicitacao_['id'] == id:
                continue

            solicitacao = solicitacao_
            break

        if not solicitacao:
            print(f'Solicitação com id {id} não encontrada') 
            return

        if not solicitacao:
            print('Solicitação não encontrada')
            return

        match opcao:
            case 1:
                solicitacao['status'] = 'ATUALIZADO'
                solicitacao['historico'].append({
                    'acao': 'Efetivado',
                    'usuario': acesso.get('usuario'),
                    'status': 'ATUALIZADO'
                })
                solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                print('Atualização efetivada com sucesso')
            case 2:
                solicitacao['status'] = 'RECUSADO'
                solicitacao['historico'].append({
                    'acao': 'Reprovado',
                    'usuario': acesso.get('usuario'),
                    'status': 'RECUSADO'
                })
                solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                print('Solicitação recusada com sucesso')
            case 3:
                ga_gn = input('Enviar para (GA/gn): ').strip().upper()
                
                match ga_gn:
                    case 'GN':
                        solicitacao['status'] = 'AJUSTE_GN'
                        solicitacao['historico'].append({
                            'acao': 'Devolvido para ajuste pelo Time de Cadastro',
                            'usuario': acesso.get('usuario'),
                            'status': 'AJUSTE_GN'
                        })
                        solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                        print('Solicitação devolvida para ajustes com sucesso')
                    case 'GA':
                        solicitacao['status'] = 'AJUSTE_GA'
                        solicitacao['historico'].append({
                            'acao': 'Devolvido para ajuste pelo Time de Cadastro',
                            'usuario': acesso.get('usuario'),
                            'status': 'AJUSTE_GA'
                        })
                        solicitacoes.salvar_solicitacao(lista_de_solicitacoes)
                        print('Solicitação devolvida para ajustes com sucesso')
                    case _:
                        print('Valor inválido')
            case _:
                print('Valor inválido')
        
    except ValueError:
        print('Escreva apenas números')
