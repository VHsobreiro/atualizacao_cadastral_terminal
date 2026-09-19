import logging

logger = logging.getLogger(__name__)

from app.dados import banco
from app.gn import consultar_solicitacao, criar_solicitacao, editar_solicitacao

banco_obj = banco.Banco()
conexao, cursor = banco_obj.obter_conexao()
buscador = banco.BuscarNoBanco(conexao=conexao, cursor=cursor)

solicitacao_obj = criar_solicitacao.SolicitacaoCadastro(buscador=buscador)

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
    print('[ 3 ] Encerrar programa')
    try:
        opcao = int(input('Sua opção: '))
        match opcao:
            case 1:
                gn_criar_solicitacao(acesso=acesso)
            case 2:
                gn_consultar_solicitacoes(acesso=acesso)
            case 3:
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

def gn_consultar_solicitacoes(acesso):
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
        print('Selecione um número positivo')

def painel_ga(usuario):
    pass

def painel_cad(usuario):
    pass