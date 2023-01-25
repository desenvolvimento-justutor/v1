# -*- coding: utf-8 -*-
import json
import requests

'''
Para ambiente de produção use a variável abaixo:
url = "https://api.focusnfe.com.br"
'''
url = "https://api.focusnfe.com.br/v2/nfse"

# Substituir pela sua identificação interna da nota
ref = {"ref": "123"}

token = "a7LYZHv1Q4B13trOu6XYJyY53CtPITRC"


def emitir():
    nfse = {
        "data_emissao": "2022-12-17T16:00:00",
        "prestador": {
            "cnpj": "24181548000143",
            "inscricao_municipal": "279.111-00",
            "codigo_municipio": "3170206"
        },
        "tomador": {
            "cpf": "88815935134",
            "razao_social": "Acras Tecnologia da Informação LTDA",
            "email": "christian.douglas.alcantara@gmail.com",
            "endereco": {
                "logradouro": "Rua Dias da Rocha Filho",
                "numero": "999",
                "complemento": "Prédio 04 - Sala 34C",
                "bairro": "Alto da XV",
                "codigo_municipio": "4106902",
                "uf": "PR",
                "cep": "80045165"
            }
        },
        "servico": {
            "aliquota": 3,
            "discriminacao": "Nota fiscal referente"
                             " a serviços \nprestados",
            "iss_retido": "false",
            "item_lista_servico": "859960500",
            "codigo_tributario_municipio": "620910000",
            "valor_servicos": 1.0,
            "desconto_condicionado": 0.2
        }
    }

    # print (json.dumps(nfse))
    r = requests.post(url, params=ref, data=json.dumps(nfse), auth=(token, ""))

    # Mostra na tela o codigo HTTP da requisicao e a mensagem de retorno da API
    print(r.status_code, r.text)


def consultar(ref):
    url = "https://api.focusnfe.com.br/v2/nfse/%s" % ref
    r = requests.delete(url, params=ref, auth=(token, ""))
    print(r.status_code, r.text)


emitir()
# consultar("12348")
