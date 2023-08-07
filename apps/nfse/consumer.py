# -*- coding: utf-8 -*-
import json
from datetime import datetime

import requests

from libs.util.cep import get_cep

# from libs.util.cep import get_cep

url = "https://api.focusnfe.com.br/v2/nfse"
token = "a7LYZHv1Q4B13trOu6XYJyY53CtPITRC"

ref = {"ref": "987"}


def hook(consulta=True):
    url = "https://api.focusnfe.com.br/v2/hooks"
    data = {
        "cnpj": "24181548000143",
        "event": "nfse",
        "url": "https://www.justutor.com.br/nfse/"
    }

    # print (json.dumps(nfse))
    if consulta:
        r = requests.get(url, auth=(token, ""))
    else:
        r = requests.post(url, data=json.dumps(data), auth=(token, ""))

    # Mostra na tela o codigo HTTP da requisicao e a mensagem de retorno da API


def emitir(ref, tomador, descriminacao, valor):
    params = {"ref": ref}
    cep_data = get_cep(tomador["endereco"]["cep"])
    tomador["endereco"]["codigo_municipio"] = cep_data["ibge"]
    nfse = {
        "data_emissao": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "prestador": {
            "cnpj": "24181548000143",
            "inscricao_municipal": "279.111-00",
            "codigo_municipio": "3170206"
        },
        "tomador": tomador,
        "servico": {
            "aliquota": 3,
            "discriminacao": descriminacao,
            "iss_retido": "false",
            "item_lista_servico": "859960500",
            "codigo_tributario_municipio": "620910000",
            "valor_servicos": valor,
        }
    }
    r = requests.post(url, params=params, data=json.dumps(nfse), auth=(token, ""))
    if r.status_code == 202:
        return r.status_code, r.json()
    else:
        return r.status_code, r.text


def consultar(ref):
    url = "https://api.focusnfe.com.br/v2/nfse/%s" % ref
    r = requests.delete(url, params=ref, auth=(token, ""))
    print(r.status_code, r.text)


if __name__ == "__main__":
    consultar("e2f6c26c25184cd5b32c61a72795de0a")