# Sistema de Atualização Cadastral no Terminal

## Colaboradores
| Nome | Função | Equipe | GitHub |
| :--- | :--- | :--- | :--- |
| **Alex** | Desenvolvedor | Time de Cadastro | [@alex-software-z09](https://github.com/alex-software-z09) |
| **Ana** | Líder e Desenvolvedora | Gerente de Negócios | [@anapontess22](https://github.com/anapontess22) |
| **Enzo** | Líder e Desenvolvedor | Dados | [@y3Enzo](https://github.com/y3Enzo) |
| **João** | Desenvolvedor | Gerente de Negócios | [@joao-victor155](https://github.com/joao-victor155) |
| **Jonaldo** | Desenvolvedor | Gerente de Agência | [@jonaldox2000](https://github.com/jonaldox2000) |
| **Kauan** | Desenvolvedor | Dados | [@kauanjesus2008](https://github.com/kauanjesus2008) |
| **Neymar** | Desenvolvedor | Time de Cadastro | [@almeidaneymar890-blip](https://github.com/almeidaneymar890-blip) |
| **Samuel** | Desenvolvedor | Gerente de Negócios | [@serpas038-oss](https://github.com/serpas038-oss) |
| **Vinicius** | Líder e Desenvolvedor | Gerente de Agência | [@Vinigentileza22](https://github.com/Vinigentileza22) |
| **Vitor** | Líder e Desenvolvedor | Time de Cadastro | [@VHsobreiro](https://github.com/VHsobreiro) |
| **Wallison** | Desenvolvedor | Gerente de Negócios | [@wallisodamasceno10-glitch](https://github.com/wallisodamasceno10-glitch) |

## Estrutura do Projeto
```text
├─ app/
│  ├─ dados/
│  │  ├─ banco/
│  │  │  ├─ banco.db
│  │  │  └─ schema.sql
│  │  ├─ solicitacoes/
│  │  │  └─ solicitacoes.json
│  │  ├─ banco.py
│  ├─ ga/
│  ├─ gn/
│  │  ├─ consultar_solicitacao.py
│  │  ├─ criar_solicitacao.py
│  │  ├─ editar_solicitacao.py
│  ├─ time_de_cadastro/
│  │  ├─ aprovacao_e_integracao_com_banco.py
│  │  ├─ devolucao_e_documentacao.py
│  │  └─ visualizar_solicitacao.py
│  ├─ __main__.py
│  └─ main.py
├─ logs/
│  └─ app.log
├─ .env
├─ .env.example
├─ .gitignore
└─ requirements.txt
```
