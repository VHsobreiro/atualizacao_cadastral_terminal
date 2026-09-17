import uuid
import sys #Bibliotecas 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #Serve para encontrar arquivos de outra pasta

from dados.banco import Banco, BuscarNoBanco


class SolicitacaoCadastro:
    def __init__(self, buscador):
        self.id = int()
        self.cliente = None
        self.tipo = None
        self.dados_antigos = None
        self.dados_novos = None     #São as listas vazias prontas para receberem informações e guardar elas
        self.criado_por = None
        self.historico = []
        self.status = None
        self._buscador = buscador

    def buscar_cliente(self, identificador): #Identifica pelo nome ou pelo cpf
        
        if not identificador:
            return False

        identificador = str(identificador).strip()

        if identificador.isdigit() and len(identificador) == 11: #Se tiver 11 número sem espaço ele indentifiica como cpf e se tiver espaço identifica como nome 
            self.cliente = self._buscador.buscar_cliente_por_cpf(identificador)
        else:
            self.cliente = self._buscador.buscar_cliente_por_nome(identificador)

        if self.cliente is None:
            return False #Busca o cliente por cpf ou nome se caso o cliente não exista retorna falso

        return True

    def selecionar_tipo(self, opcao): #Tipos de solicitação
        tipos_disponiveis = {
            "1": "Renda",
            "2": "Patrimônio",
            "3": "Endereço",
        }

        if opcao not in tipos_disponiveis: #Se a opção informada não existir retorna falso
            return False

        self.tipo = tipos_disponiveis[opcao] #Se o tipo existir retorna true
        return True

    def criar_solicitacao(self, usuario_logado=None, identificador_cliente=None, opcao_tipo=None):#Serve para preencher as informações que estão vazias e fazer que o código não quebre por falta de informações
        
        if not identificador_cliente: 
            self.status = "erro_cliente_nao_informado"
            return False

        if not self.buscar_cliente(identificador_cliente):
            self.status = "erro_cliente_nao_encontrado"
            return False

        if not opcao_tipo or not self.selecionar_tipo(opcao_tipo):
            self.status = "erro_tipo_invalido"
            return False #Este bloco de código indentifica se o cliente existe, caso não exista retorna que o cliente não foi encontrado

        campo_no_bd = self.tipo.lower() #Pega a opcão escolhida exemplo "Renda" e deixa minúscula, pois é assim que está no banco de dados
        self.dados_antigos = self.cliente.get(campo_no_bd) if isinstance(self.cliente, dict) else None #Descobre qual a informação antiga do cliente antes da mudança

        self.criado_por = usuario_logado #Mostra o usuário logado
        self.status = "pendente" #Mostra o status da solicitação

        self.historico.append({
            "acao": "criação",
            "usuario": usuario_logado,
            "status": self.status #Mostra como está o histórico da solicitação
        })

        return True #Retorna verdadeiro

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "tipo": self.tipo,
            "dados_antigos": self.dados_antigos,
            "dados_novos": self.dados_novos,
            "criado_por": self.criado_por,
            "historico": self.historico,
            "status": self.status, #Essa parte serve para empacotar todas as informações do pedido e entregá-las em formato de lista/dicionário.
        }


if __name__ == "__main__": #Essa linha significa: "Só rode o código abaixo se eu executar ESTE arquivo diretamente
    try:
        conexao, cursor = Banco.obter_conexao() #Faz a conexão com o banco de dados onde as informações estão guardadas
        buscador = BuscarNoBanco(conexao, cursor) #Sempre que precisar achar um cpf ou nome o buscador vai procurar e trazer essas informações de volta

        s = SolicitacaoCadastro(buscador) #ele abre o sistema, conecta no banco de dados, cria um pedido de mudança de cadastro, valida os dados e mostra o resultado final na tela de forma segura

   
        sucesso = s.criar_solicitacao(identificador_cliente='test0', opcao_tipo="1") #Cria a solicitação e mostra os dados do cliente na tela

        if sucesso:
            print(f"Solicitação {s.id} criada com sucesso!") #Se a solicitação foi criada corretamente aparece esse print na tela
            print(s.to_dict())
        else:
            print(f"Falha ao criar solicitação: {s.status}") #Se não foi criada corretamente aparece isso na tela

        if hasattr(buscador, "fechar_conexao"): #medida de segurança que desliga a conexão com o banco de dados sem quebrar o programa
            buscador.fechar_conexao()

    except Exception as e:
        print(f"Erro ao executar a conexão com o banco: {e}") #Essa linha é uma trava de segurança contra falhas inesperadas